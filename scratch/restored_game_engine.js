// 9. PAINEL DE RECEITA ESTILO TV FIXADO NA PAREDE
1368:         // ==========================================
1369:         let recipeBoardMesh = null;
1370:         let recipeCanvasCtx = null;
1371:         let recipeTexture = null;
1372: 
1373:         function createRecipeBoard() {
1374:             const canvas = document.createElement('canvas');
1375:             canvas.width = 600;
1376:             canvas.height = 360;
1377:             recipeCanvasCtx = canvas.getContext('2d');
1378: 
1379:             recipeTexture = new THREE.CanvasTexture(canvas);
1380:             const boardGeo = new THREE.PlaneGeometry(0.90, 0.54);
1381:             const boardMat = new THREE.MeshBasicMaterial({ map: recipeTexture, transparent: true });
1382:             recipeBoardMesh = new THREE.Mesh(boardGeo, boardMat);
1383:             recipeBoardMesh.position.set(0.0, 1.68, -1.87);
1384:             scene.add(recipeBoardMesh);
1385: 
1386:             updateRecipeBoard();
1387:         }
1388: 
1389:         function updateRecipeBoard() {
1390:             if (!recipeCanvasCtx) return;
1391: 
1392:             const ctx = recipeCanvasCtx;
1393:             ctx.clearRect(0, 0, 600, 360);
1394: 
1395:             ctx.fillStyle = '#1B2A4A';
1396:             ctx.roundRect(10, 10, 580, 340, 18);
1397:             ctx.fill();
1398: 
1399:             ctx.lineWidth = 8;
1400:             ctx.strokeStyle = '#20B2AA';
1401:             ctx.roundRect(10, 10, 580, 340, 18);
1402:             ctx.stroke();
1403: 
1404:             const recipe = gameEngine.getCurrentRecipe();
1405: 
1406:             ctx.fillStyle = '#FFD700';
1407:             ctx.font = 'bold 26px "Outfit", sans-serif';
1408:             ctx.fillText(`RECEITA: ${recipe.name.toUpperCase()}`, 30, 55);
1409: 
1410:             ctx.font = '20px "Outfit", sans-serif';
1411: 
1412:             let yOffset = 110;
1413:             recipe.steps.forEach((step, idx) => {
1414:                 const isCompleted = gameEngine.stackedItems.length > idx;
1415:                 const isCurrent = gameEngine.stackedItems.length === idx;
1416: 
1417:                 if (isCompleted) {
1418:                     ctx.fillStyle = '#06D6A0';
1419:                     ctx.fillText(`✓ ${idx + 1}. ${step.label}`, 30, yOffset);
1420:                 } else if (isCurrent) {
1421:                     ctx.fillStyle = '#FFD700';
1422:                     ctx.fillText(`▶ ${idx + 1}. ${step.label}`, 30, yOffset);
1423:                 } else {
1424:                     ctx.fillStyle = '#A0AEC0';
1425:                     ctx.fillText(`  ${idx + 1}. ${step.label}`, 30, yOffset);
1426:                 }
1427:                 yOffset += 42;
1428:             });
1429: 
1430:             recipeTexture.needsUpdate = true;
1431:         }
1432: 
1433:         // ==========================================
1434:         // 10. GERENCIADOR DE JOGABILIDADE E RECEITAS
1435:         // ==========================================
1436:         const RECIPES = {
1437:             classic: {
1438:                 name: "Hambúrguer Clássico",
1439:                 steps: [
1440:                     { type: 'bottom-pao', label: 'Pão de Baixo' },
1441:                     { type: 'carne-burger', label: 'Carne Grelhada' },
1442:                     { type: 'fatia-queijo', label: 'Queijo Fatiado' },
1443:                     { type: 'burger-top', label: 'Pão de Cima' }
1444:                 ]
1445:             },
1446:             double: {
1447:                 name: "Cheeseburger Duplo",
1448:                 steps: [
1449:                     { type: 'bottom-pao', label: 'Pão de Baixo' },
1450:                     { type: 'carne-burger', label: 'Carne Grelhada (1ª)' },
1451:                     { type: 'fatia-queijo', label: 'Queijo Fatiado (1º)' },
1452:                     { type: 'carne-burger', label: 'Carne Grelhada (2ª)' },
1453:                     { type: 'fatia-queijo', label: 'Queijo Fatiado (2º)' },
1454:                     { type: 'burger-top', label: 'Pão de Cima' }
1455:                 ]
1456:             }
1457:         };
1458: 
1459:         class GameEngine {
1460:             constructor() {
1461:                 this.currentRecipeKey = 'classic';
1462:                 this.score = 0;
1463:                 this.timeLeft = 60;
1464:                 this.timerInterval = null;
1465:                 this.stackedItems = [];
1466:                 this.assemblyHeight = 0.9320; // Base do prato central em Y = 0.9220 + 0.010 = 0.9320
1467:                 this.isPlaying = true;
1468: 
1469:                 this.initTimer();
1470:             }
1471: 
1472:             getCurrentRecipe() {
1473:                 return RECIPES[this.currentRecipeKey];
1474:             }
1475: 
1476:             setRecipe(key) {
1477:                 this.currentRecipeKey = key;
1478:                 this.resetAssembly();
1479:                 updateRecipeBoard();
1480:             }
1481: 
1482:             initTimer() {
1483:                 if (this.timerInterval) clearInterval(this.timerInterval);
1484:                 this.timeLeft = 60;
1485:                 this.updateTimerUI();
1486: 
1487:                 this.timerInterval = setInterval(() => {
1488:                     if (!this.isPlaying) return;
1489:                     this.timeLeft--;
1490:                     this.updateTimerUI();
1491: 
1492:                     if (this.timeLeft <= 0) {
1493:                         this.handleTimeOut();
1494:                     }
1495:                 }, 1000);
1496:             }
1497: 
1498:             startTimer() {
1499:                 this.initTimer();
1500:             }
1501: 
1502:             updateTimerUI() {
1503:                 const el = document.getElementById('timer-val');
1504:                 const box = document.getElementById('timer-box');
1505:                 if (el) el.innerText = this.timeLeft;
1506: 
1507:                 if (this.timeLeft <= 15) {
1508:                     box.classList.add('warning');
1509:                 } else {
1510:                     box.classList.remove('warning');
1511:                 }
1512:             }
1513: 
1514:             addScore(pts) {
1515:                 this.score += pts;
1516:                 document.getElementById('score-val').innerText = this.score;
1517:             }
1518: 
1519:             resetAssembly() {
1520:                 this.stackedItems.forEach(item => {
1521:                     scene.remove(item.mesh);
1522:                 });
1523:                 this.stackedItems = [];
1524:                 this.assemblyHeight = 0.9320;
1525: 
1526:                 if (pattyController) pattyController.reset();
1527: 
1528:                 resetAllTrayIngredients();
1529:                 updateRecipeBoard();
1530:             }
1531: 
1532:             trySnapToPlate(itemObj) {
1533:                 const recipe = this.getCurrentRecipe();
1534:                 const nextStepIdx = this.stackedItems.length;
1535: 
1536:                 if (nextStepIdx >= recipe.steps.length) return false;
1537: 
1538:                 const expectedType = recipe.steps[nextStepIdx].type;
1539: 
1540:                 if (itemObj.type === expectedType) {
1541:                     audioManager.playPop();
1542: 
1543:                     const platePos = new THREE.Vector3(0.0, this.assemblyHeight, -0.65);
1544:                     vfxManager.addLerp(itemObj.mesh, platePos);
1545: 
1546:                     const heights = {
1547:                         'bottom-pao': 0.032,
1548:                         'carne-burger': 0.024,
1549:                         'fatia-queijo': 0.008,
1550:                         'burger-top': 0.045
1551:                     };
1552:                     this.assemblyHeight += (heights[itemObj.type] || 0.02);
1553: 
1554:                     this.stackedItems.push(itemObj);
1555: 
1556:                     const idx = interactiveItems.indexOf(itemObj);
1557:                     if (idx !== -1) interactiveItems.splice(idx, 1);
1558: 
1559:                     updateRecipeBoard();
1560: 
1561:                     if (itemObj.type === 'carne-burger' && pattyController) {
1562:                         pattyController.onPattyPlacedOnPlate();
1563:                     } else {
1564:                         spawnSingleTrayReplacement(itemObj.type);
1565:                     }
1566: 
1567:                     if (this.stackedItems.length === recipe.steps.length) {
1568:                         this.handleVictory();
1569:                     }
1570:                     return true;
1571:                 } else {
1572:                     return false;
1573:                 }
1574:             }
1575: 
1576:             verifyOrder() {
1577:                 const recipe = this.getCurrentRecipe();
1578:                 if (!recipe) return false;
1579:                 const isComplete = this.stackedItems.length === recipe.steps.length;
1580:                 if (isComplete) {
1581:                     this.handleVictory();
1582:                 }
1583:                 return isComplete;
1584:             }
1585: 
1586:             handleVictory() {
1587:                 this.isPlaying = false;
1588:                 audioManager.playVictoryFanfare();
1589:                 vfxManager.spawnConfetti();
1590: 
1591:                 const bonusPoints = 1000 + (this.timeLeft * 25);
1592:                 this.addScore(bonusPoints);
1593: 
1594:                 document.getElementById('victory-score-val').innerText = `+${bonusPoints} pts`;
1595:                 document.getElementById('victory-modal').classList.add('active');
1596:             }
1597: 
1598:             handleTimeOut() {
1599:                 this.isPlaying = false;
1600:                 if (pattyController && pattyController.state === 1) {
1601:                     audioManager.stopSizzle();
1602:                     vfxManager.stopSmoke();
1603:                 }
1604:                 document.getElementById('fail-modal').classList.add('active');
1605:             }
1606: 
1607:             restartOrder() {
1608:                 this.resetAssembly();
1609:                 this.isPlaying = true;
1610:                 this.initTimer();
1611:                 document.getElementById('victory-modal').classList.remove('active');
1612:                 document.getElementById('fail-modal').classList.remove('active');
1613:             }
1614:         }
1615: 
1616:         // ==========================================
1617:         