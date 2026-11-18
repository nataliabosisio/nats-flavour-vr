<?php
header('Content-Type: application/json; charset=utf-8');
require_once __DIR__ . '/../db.php';

$data = json_decode(file_get_contents('php://input'), true);
$nome = trim($data['nome'] ?? '');

if (empty($nome)) {
    http_response_code(400);
    echo json_encode(['mensagem' => 'Nome é obrigatório.']);
    exit;
}

try {
    // Busca se o utilizador já existe na base de dados
    $stmt = $mysqli->prepare("SELECT id, nome FROM usuarios WHERE LOWER(nome) = LOWER(?)");
    $stmt->bind_param("s", $nome);
    $stmt->execute();
    $result = $stmt->get_result();

    if ($row = $result->fetch_assoc()) {
        echo json_encode($row);
        exit;
    }

    // Se não existir, insere o novo utilizador
    $stmtInsert = $mysqli->prepare("INSERT INTO usuarios (nome) VALUES (?)");
    $stmtInsert->bind_param("s", $nome);
    $stmtInsert->execute();

    echo json_encode([
        'id' => $stmtInsert->insert_id,
        'nome' => $nome
    ]);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['mensagem' => 'Erro no servidor: ' . $e->getMessage()]);
}