# 網頁按鈕：綠燈閃三次（socket v5）

網站底部新增「綠燈閃三次」，沿用現有按鈕樣式。按下後，ESP32 的 RGB LED 綠燈亮 300 ms、滅 300 ms，重複三次，約 1.8 秒後恢復原本顏色；原本關燈則恢復關燈。實際時間受 20 ms 控制排程與系統負載影響。

## 操作方式

1. 等 LED 狀態顯示「LED 可操作」。
2. 按「綠燈閃三次」。閃爍期間，綠燈按鈕與切換 LED 按鈕暫停操作。
3. 狀態顯示「綠燈閃爍中：3 次，請稍候」。命令完成後顯示「綠燈已閃三次，已恢復原狀」。

AUTO、MANUAL 都能使用。光照紅燈警示進行中時，不能插入綠燈；綠燈執行中時，低光任務會稍後重試紅燈警示，兩者不會同時寫入 GPIO。綠燈不增加原本的閃紅計數。重複點擊或其他來源的改色在忙碌期間回覆 busy，不排隊到閃完後突然改色。

斷線或請求逾時會顯示「LED 操作結果未知」，不會自動重送可能已經執行的閃燈命令。LED 狀態未知或超過有效期限時，兩個 LED 按鈕都停用。此操作狀態與原本一般感測資料分流。

## 更新已安裝 socket v3／v4 的 ESP32

下載 `IoT_Course_socket_ESP32_v5_green_patch.zip`，解壓縮後在 Thonny 按停止，將以下四個檔案上傳至 ESP32，保留相同路徑並覆蓋：

```text
/index.html
/runtime/services/led_controller.mpy
/runtime/tasks.mpy
/runtime/hardware/motion.mpy
```

後兩個檔案沿用前次的 PIR 移入／移出功能，讓 v3 或 v4 都能直接更新。更新包不包含 config.py，保留你目前的網路、腳位和光照設定。說明文件與 manifest 留在電腦即可。

上傳後重新啟動 ESP32，再在網站按 Ctrl+F5 重新整理；手機可關閉分頁後重新開啟。更新檔採 MicroPython v1.29.0／MPY v6.3 可攜式編譯，對應已提供的韌體資訊。Boot／Main 仍沿用 socket-v3 字樣。

首次安裝或未使用前述 socket 版本，改用完整 `IoT_Course_socket_ESP32_v5_mpy129.zip`，依 UPLOAD_README.md 安裝；已有裝置設定時保留裝置上的 config.py。

## 程式位置與 API

- index.html：新增 greenBlinkButton、blinkGreen()，透過原有命令 API 提交 JSON。
- services/led_controller.py：加入 blink_green，仍由唯一 LedController 分階段切換綠／關，沒有在 HTTP handler 等待整段閃燈。
- 原有 `POST /api/led/commands` 使用 `{"kind":"blink_green"}`，回覆 202 表示受理；既有 `GET /api/led/commands/ID` 查詢 accepted、executing、executed 或失敗。
- LED 快照新增 busy、effect_kind、green_blink_active；alert_active 仍只表示低光紅燈警示。
- 正在執行的命令紀錄不會被持續 busy 回覆擠掉，總紀錄仍限制 16 筆，以便網站取得完成結果。

## 驗證與回復

79 項 Python 桌面測試與兩組 Node 前端測試通過。新增檢查實際綠／滅輸出三次、恢復顏色與關燈、MANUAL、時間計數器回繞、忙碌互斥、低光重試、命令紀錄保留、停止清理、GPIO 錯誤，以及真實本機 TCP API 的受理／執行／完成查詢。網站測試涵蓋按鈕 JSON、重複點擊、警示衝突、完成提示、逾時與不自動重送；既有 PIR、RFID、MQTT、圖表及啟動測試亦通過。

尚未連接使用者的 ESP32，實際燈色與三次閃爍仍需上傳後確認。交叉編譯與桌面 fake GPIO 不等同實機驗證。

回復至 v4 時，從保留的 v4 完整 ZIP 取回 index.html 與 runtime/services/led_controller.mpy，覆蓋並重啟即可；私人 config 不需變更。原始碼修改前公開備份為 mdy_07，不部署備份資料夾。
