<?php
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);

$mysqli = mysqli_connect('localhost', 'root', '', 'nats_flavour_vr');
mysqli_set_charset($mysqli, 'utf8mb4');