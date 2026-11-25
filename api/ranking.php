<?php
header('Content-Type: application/json; charset=utf-8');
require_once __DIR__ . '/../db.php';

try {
    // Trocado MAX(p.pontuacao) por SUM(p.pontuacao) para somar o total de partidas
    $query = "
SELECT u.nome, COALESCE(SUM(p.pontuacao), 0) AS pontuacao
FROM usuarios u
LEFT JOIN partidas p ON p.usuario_id = u.id
GROUP BY u.id, u.nome
ORDER BY pontuacao DESC, u.id ASC;
    ";

    $result = $mysqli->query($query);
    $ranking = [];

    while ($row = $result->fetch_assoc()) {
        $ranking[] = [
            'nome' => $row['nome'],
            'pontuacao' => (int)$row['pontuacao']
        ];
    }

    echo json_encode($ranking);
} catch (Exception $e) {
    http_response_code(500);
    echo json_encode(['mensagem' => 'Erro ao procurar ranking: ' . $e->getMessage()]);
}