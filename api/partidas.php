<?php
header('Content-Type: application/json; charset=utf-8');
require_once __DIR__ . '/../db.php';

$data = json_decode(file_get_contents('php://input'), true);

$usuario_id = $data['usuario_id'] ?? null;
$receita = $data['receita'] ?? '';
$pontuacao = isset($data['pontuacao']) ? (int)$data['pontuacao'] : 0;
$tempo_restante = isset($data['tempo_restante']) ? (int)$data['tempo_restante'] : 0;
// Se o status não for informado pela requisição, define automaticamente
$status = $data['status'] ?? ($tempo_restante > 0 ? 'vitoria' : 'derrota');

if (!$usuario_id) {
    http_response_code(400);
    echo json_encode(['mensagem' => 'ID do utilizador é obrigatório.']);
    exit;
}

try {
    $stmt = $mysqli->prepare("INSERT INTO partidas (usuario_id, receita, pontuacao, tempo_restante, status) VALUES (?, ?, ?, ?, ?)");
    $stmt->bind_param("isiis", $usuario_id, $receita, $pontuacao, $tempo_restante, $status);
    $stmt->execute();

    echo json_encode(['mensagem' => 'Partida gravada com sucesso!']);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['mensagem' => 'Erro ao gravar partida: ' . $e->getMessage()]);
}