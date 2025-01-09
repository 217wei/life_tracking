# Life_tracking

This is the final project for Database Systems course in NCCU 2025 fall. The project aims to design a database for tracking health information. 

## Table of Contents
- [Project Overview](#project-overview)
- [Team](#Team)
- [Requirements Analysis](#requirements-analysis)
- [System Function](#system-function)

## Team
- 林青欣  教碩二  
- 李冠蓁  資訊三  
- 李采萱  資訊三  
- 林子葳  資訊三  
- 宋庭萱  統計四  
- 呂承恩  應數碩一



## Requirements Analysis
- 使用者可以從首頁登入註冊帳號，輸入基本資料（身高、體重、出生日期、電話、姓名、性別）。
- 登入之後，會有自己的使用者ID。
- 使用者可以每天記錄自己健康狀況（體重、睡眠…）。
- 使用者可以設定目標，包含達成及開始執行日期。
- 使用者可以更改或刪除健康紀錄、目標。
- 使用者可以建立醫療紀錄、家族病史。
- 使用者可以自行輸入營養進食份數（碳水、蛋白質、油脂），系統計算後，記錄在當天進食熱量。
- 系統提供運動選項讓使用者選擇當天記錄。
- 運動分成有氧及無氧。

## System Function
使用者可以註冊自己的帳號，並輸入的健康資料，每日可以更新當天健康記錄，寫入自己攝入的營養份數和運動。使用者也可以設定目標，作爲執行時間參考。每日記錄及目標都可以被更新或是刪除。
- 資料庫模組：使用者資料、醫療病史、目標記錄、每日健康記錄、睡眠記錄、飲食記錄
- 資料庫新增、查詢修改刪除：將目標加入或移除目標記錄、健康記錄