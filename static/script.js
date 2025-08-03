// グローバル変数
let currentMatchId = null;
let currentTurn = 1;
let playerA = '';
let playerB = '';
let currentPlayer = '';
let currentTurnData = {
    normal_cards: [],
    act_cards: []
};

// API ベースURL
const API_BASE = '/api';

// レアリティとエーテル値のマッピング
const RARITY_ETHER = {
    'bronze': 200,
    'silver': 400,
    'gold': 800,
    'legend': 3500
};

// レアリティ表示名
const RARITY_NAMES = {
    'bronze': 'ブロンズ',
    'silver': 'シルバー',
    'gold': 'ゴールド',
    'legend': 'レジェンド'
};

// ユーティリティ関数
function showElement(id) {
    document.getElementById(id).style.display = 'block';
}

function hideElement(id) {
    document.getElementById(id).style.display = 'none';
}

function showAlert(message, type = 'info') {
    alert(message);
}

// スコア表示更新
function updateScoreDisplay(turn, player, totalScores, finalScores = null) {
    document.getElementById('currentTurn').textContent = turn;
    document.getElementById('currentPlayer').textContent = player;
    document.getElementById('playerAScore').textContent = finalScores ? finalScores[playerA] : totalScores[playerA];
    document.getElementById('playerBScore').textContent = finalScores ? finalScores[playerB] : totalScores[playerB];
}

// プレイヤー名の入力時にセレクトボックスを更新
function updateFirstPlayerOptions() {
    const playerAInput = document.getElementById('playerA');
    const playerBInput = document.getElementById('playerB');
    const firstPlayerSelect = document.getElementById('firstPlayer');
    
    const playerAName = playerAInput.value.trim();
    const playerBName = playerBInput.value.trim();
    
    firstPlayerSelect.innerHTML = '<option value="">選択してください</option>';
    
    if (playerAName) {
        firstPlayerSelect.innerHTML += `<option value="${playerAName}">${playerAName}</option>`;
    }
    if (playerBName) {
        firstPlayerSelect.innerHTML += `<option value="${playerBName}">${playerBName}</option>`;
    }
}

// プレイヤー名入力のイベントリスナーを設定
document.addEventListener('DOMContentLoaded', function() {
    const playerAInput = document.getElementById('playerA');
    const playerBInput = document.getElementById('playerB');
    
    if (playerAInput && playerBInput) {
        playerAInput.addEventListener('input', updateFirstPlayerOptions);
        playerBInput.addEventListener('input', updateFirstPlayerOptions);
    }
    
    loadHistory();
});

// 新規対戦開始
async function startNewMatch() {
    playerA = document.getElementById('playerA').value.trim();
    playerB = document.getElementById('playerB').value.trim();
    const firstPlayer = document.getElementById('firstPlayer').value;
    
    if (!playerA || !playerB) {
        showAlert('両方のプレイヤー名を入力してください');
        return;
    }
    
    if (!firstPlayer) {
        showAlert('先行プレイヤーを選択してください');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/match/new`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                player_a: playerA, 
                player_b: playerB,
                first_player: firstPlayer
            })
        });

        if (!response.ok) {
            throw new Error('対戦作成に失敗しました');
        }

        const match = await response.json();
        currentMatchId = match.id;
        currentPlayer = firstPlayer;
        currentTurn = 1;

        // UI切り替え
        hideElement('matchStart');
        showElement('matchActive');
        
        // プレイヤー名を表示
        document.getElementById('playerAName').textContent = playerA;
        document.getElementById('playerBName').textContent = playerB;
        document.getElementById('playerANameScore').textContent = playerA;
        document.getElementById('playerBNameScore').textContent = playerB;
        document.getElementById('playerANameFinish').textContent = playerA;
        document.getElementById('playerBNameFinish').textContent = playerB;
        
        updateScoreDisplay(1, currentPlayer, {[playerA]: 0, [playerB]: 0});
        clearCurrentTurn();

    } catch (error) {
        showAlert(`エラー: ${error.message}`);
    }
}

// 通常カード追加（フォロワー・スペル・アミュレット）
async function addNormalCard(rarity) {
    if (!currentMatchId) {
        showAlert('対戦が開始されていません');
        return;
    }

    const etherValue = RARITY_ETHER[rarity];
    
    // ローカルのターンデータに追加
    currentTurnData.normal_cards.push({rarity, etherValue});
    
    try {
        const response = await fetch(`${API_BASE}/match/${currentMatchId}/button`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                player: currentPlayer,
                rarity: rarity,
                card_type: 'follower', // 通常カードはフォロワーとして扱う
                ether_value: etherValue
            })
        });

        if (!response.ok) {
            throw new Error('ポイント追加に失敗しました');
        }

        const result = await response.json();
        
        // 表示を更新
        updateCurrentTurnDisplay();
        updateScoreDisplay(result.current_turn, result.current_player, result.total_scores, result.final_scores);

    } catch (error) {
        // エラー時はローカルデータを元に戻す
        currentTurnData.normal_cards.pop();
        showAlert(`エラー: ${error.message}`);
    }
}

// アクトカード追加
async function addActCard(rarity) {
    if (!currentMatchId) {
        showAlert('対戦が開始されていません');
        return;
    }

    const etherValue = RARITY_ETHER[rarity];
    const actualScore = Math.floor(etherValue / 3); // 1/3計算（切り捨て）
    
    // ローカルのターンデータに追加
    currentTurnData.act_cards.push({rarity, etherValue, actualScore});
    
    try {
        const response = await fetch(`${API_BASE}/match/${currentMatchId}/button`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                player: currentPlayer,
                rarity: rarity,
                card_type: 'act',
                ether_value: etherValue
            })
        });

        if (!response.ok) {
            throw new Error('ポイント追加に失敗しました');
        }

        const result = await response.json();
        
        // 表示を更新
        updateCurrentTurnDisplay();
        updateScoreDisplay(result.current_turn, result.current_player, result.total_scores, result.final_scores);

    } catch (error) {
        // エラー時はローカルデータを元に戻す
        currentTurnData.act_cards.pop();
        showAlert(`エラー: ${error.message}`);
    }
}

// 現在ターンの表示を更新
function updateCurrentTurnDisplay() {
    const container = document.getElementById('currentTurnInputs');
    container.innerHTML = '';
    
    // 通常カードを表示
    currentTurnData.normal_cards.forEach((card, index) => {
        const div = document.createElement('div');
        div.className = 'turn-input-item normal';
        div.innerHTML = `
            <span class="rarity ${card.rarity}">${RARITY_NAMES[card.rarity]}</span>
            <span class="card-type">通常</span>
            <span class="ether-value">${card.etherValue}</span>
            <button class="remove-btn" onclick="removeNormalCard(${index})">×</button>
        `;
        container.appendChild(div);
    });
    
    // アクトカードを表示
    currentTurnData.act_cards.forEach((card, index) => {
        const div = document.createElement('div');
        div.className = 'turn-input-item act';
        div.innerHTML = `
            <span class="rarity ${card.rarity}">${RARITY_NAMES[card.rarity]}</span>
            <span class="card-type">アクト</span>
            <span class="ether-value">${card.etherValue} → ${card.actualScore}</span>
            <button class="remove-btn" onclick="removeActCard(${index})">×</button>
        `;
        container.appendChild(div);
    });
    
    // スコア計算
    const normalScore = currentTurnData.normal_cards.reduce((sum, card) => sum + card.etherValue, 0);
    const actScore = currentTurnData.act_cards.reduce((sum, card) => sum + card.actualScore, 0);
    const totalScore = normalScore + actScore;
    
    document.getElementById('normalScore').textContent = normalScore;
    document.getElementById('actScore').textContent = actScore;
    document.getElementById('turnScore').textContent = totalScore;
}

// 通常カードを削除
function removeNormalCard(index) {
    currentTurnData.normal_cards.splice(index, 1);
    updateCurrentTurnDisplay();
    // サーバーと同期
    syncWithServer();
}

// アクトカードを削除
function removeActCard(index) {
    currentTurnData.act_cards.splice(index, 1);
    updateCurrentTurnDisplay();
    // サーバーと同期
    syncWithServer();
}

// サーバーとの同期
async function syncWithServer() {
    if (!currentMatchId) return;
    
    try {
        const response = await fetch(`${API_BASE}/match/${currentMatchId}/score`);
        if (response.ok) {
            const result = await response.json();
            updateScoreDisplay(result.current_turn, result.current_player, result.total_scores, result.final_scores);
        }
    } catch (error) {
        console.log('同期エラー:', error);
    }
}

// 現在のターンをクリア
function clearCurrentTurn() {
    currentTurnData = {
        normal_cards: [],
        act_cards: []
    };
    updateCurrentTurnDisplay();
}

// 次のターン
async function nextTurn() {
    if (!currentMatchId) {
        showAlert('対戦が開始されていません');
        return;
    }

    try {
        // 現在のスコアを取得して次のプレイヤーを確認
        const response = await fetch(`${API_BASE}/match/${currentMatchId}/score`);
        if (!response.ok) {
            throw new Error('スコア取得に失敗しました');
        }

        const result = await response.json();
        currentPlayer = result.current_player;
        currentTurn = result.current_turn;
        
        updateScoreDisplay(result.current_turn, result.current_player, result.total_scores, result.final_scores);
        
        // 現在ターンの入力をクリア
        clearCurrentTurn();

    } catch (error) {
        showAlert(`エラー: ${error.message}`);
    }
}

// 1ターン戻る
async function undoTurn() {
    if (!currentMatchId) {
        showAlert('対戦が開始されていません');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/match/${currentMatchId}/turn/last`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('ターン削除に失敗しました');
        }

        const result = await response.json();
        currentPlayer = result.current_player;
        currentTurn = result.current_turn;
        
        updateScoreDisplay(result.current_turn, result.current_player, result.total_scores, result.final_scores);
        
        // 現在ターンの入力をクリア
        clearCurrentTurn();

    } catch (error) {
        showAlert(`エラー: ${error.message}`);
    }
}

// 対戦履歴を表示
async function showMatchHistory() {
    if (!currentMatchId) {
        showAlert('対戦が開始されていません');
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/match/${currentMatchId}/history`);
        if (!response.ok) {
            throw new Error('履歴取得に失敗しました');
        }

        const turns = await response.json();
        displayMatchHistory(turns);
        showElement('historyModal');

    } catch (error) {
        showAlert(`エラー: ${error.message}`);
    }
}

// 対戦履歴を表示
function displayMatchHistory(turns) {
    const container = document.getElementById('matchHistoryContent');
    
    if (turns.length === 0) {
        container.innerHTML = '<p>まだターンがありません</p>';
        return;
    }

    container.innerHTML = turns.map(turn => {
        const followers = turn.defeated_followers.join(', ') || '0';
        const spells = turn.used_spells.join(', ') || '0';
        const amulets = turn.used_amulets.join(', ') || '0';
        const acts = turn.acted_amulets.join(', ') || '0';
        
        return `
            <div class="history-turn">
                <div class="turn-header">
                    <h4>ターン ${turn.turn_number} - ${turn.player}</h4>
                    <button class="edit-button" onclick="editTurn(${turn.turn_number})">編集</button>
                </div>
                <div class="turn-details">
                    <div>フォロワー: ${followers}</div>
                    <div>スペル: ${spells}</div>
                    <div>アミュレット: ${amulets}</div>
                    <div>アクト: ${acts}</div>
                </div>
            </div>
        `;
    }).join('');
}

// ターン編集
let editingTurnNumber = null;

function editTurn(turnNumber) {
    editingTurnNumber = turnNumber;
    // ここでターン編集モーダルを開く
    showElement('editTurnModal');
    // 実際の編集機能は将来的に実装
    document.getElementById('editTurnContent').innerHTML = `
        <p>ターン ${turnNumber} の編集機能は開発中です。</p>
        <p>現在は「1ターン戻る」機能をご利用ください。</p>
    `;
}

function closeEditTurnModal() {
    hideElement('editTurnModal');
    editingTurnNumber = null;
}

function saveEditedTurn() {
    // 編集保存機能は将来的に実装
    showAlert('編集機能は開発中です');
    closeEditTurnModal();
}

function deleteTurn() {
    // ターン削除機能は将来的に実装
    showAlert('個別ターン削除機能は開発中です');
}

// 履歴モーダルを閉じる
function closeHistoryModal() {
    hideElement('historyModal');
}

// 対戦終了
async function finishMatch(winner) {
    if (!currentMatchId) {
        showAlert('対戦が開始されていません');
        return;
    }

    const winnerName = winner === 'playerA' ? playerA : playerB;

    try {
        const response = await fetch(`${API_BASE}/match/${currentMatchId}/finish`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ winner: winnerName })
        });

        if (!response.ok) {
            throw new Error('対戦終了に失敗しました');
        }

        const match = await response.json();
        showAlert(`${winnerName} の勝利！\n最終スコア: ${winnerName}: ${match.total_scores[winnerName]}, ${winner === 'playerA' ? playerB : playerA}: ${match.total_scores[winner === 'playerA' ? playerB : playerA]}`);

        // UI をリセット
        hideElement('matchActive');
        showElement('matchStart');
        document.getElementById('playerA').value = '';
        document.getElementById('playerB').value = '';
        document.getElementById('firstPlayer').innerHTML = '<option value="">選択してください</option>';
        currentMatchId = null;
        currentTurn = 1;
        playerA = '';
        playerB = '';
        currentPlayer = '';
        clearCurrentTurn();

        // 履歴を更新
        loadHistory();

    } catch (error) {
        showAlert(`エラー: ${error.message}`);
    }
}

// 対戦履歴読み込み
async function loadHistory() {
    try {
        const response = await fetch(`${API_BASE}/match/list`);
        if (!response.ok) {
            throw new Error('履歴取得に失敗しました');
        }

        const matches = await response.json();
        displayHistory(matches);

    } catch (error) {
        showAlert(`エラー: ${error.message}`);
    }
}

// 履歴表示
function displayHistory(matches) {
    const container = document.getElementById('historyList');
    
    if (matches.length === 0) {
        container.innerHTML = '<p>対戦履歴がありません</p>';
        return;
    }

    container.innerHTML = matches.map(match => {
        const date = new Date(match.date).toLocaleString('ja-JP');
        const winner = match.winner || '未完了';
        const playerAScore = match.total_scores[match.players[0]] || 0;
        const playerBScore = match.total_scores[match.players[1]] || 0;

        return `
            <div class="history-item">
                <div class="history-info">
                    <div class="history-players">${match.players[0]} vs ${match.players[1]}</div>
                    <div class="history-date">${date}</div>
                    <div class="history-winner">勝者: ${winner}</div>
                </div>
                <div class="history-scores">
                    <div>${match.players[0]}: ${playerAScore}</div>
                    <div>${match.players[1]}: ${playerBScore}</div>
                </div>
                <div class="history-actions">
                    <button onclick="editMatch('${match.id}')">編集</button>
                    <button onclick="deleteMatch('${match.id}')">削除</button>
                </div>
            </div>
        `;
    }).join('');
}

// 対戦編集
function editMatch(matchId) {
    showElement('editMatchModal');
    document.getElementById('editMatchContent').innerHTML = `
        <p>対戦 ${matchId} の編集機能は開発中です。</p>
        <p>現在は削除機能のみご利用いただけます。</p>
        <button onclick="closeEditMatchModal()">閉じる</button>
    `;
}

function closeEditMatchModal() {
    hideElement('editMatchModal');
}

// 対戦削除
async function deleteMatch(matchId) {
    if (!confirm('この対戦を削除しますか？')) {
        return;
    }

    try {
        const response = await fetch(`${API_BASE}/match/${matchId}`, {
            method: 'DELETE'
        });

        if (!response.ok) {
            throw new Error('対戦削除に失敗しました');
        }

        loadHistory();

    } catch (error) {
        showAlert(`エラー: ${error.message}`);
    }
}
