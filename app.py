import json
import os
import socket
import threading
import time
import uuid
from pathlib import Path
import urllib.request
import urllib.error
import streamlit as st
import streamlit.components.v1 as components

import base64
import io
import re
import hmac
import sqlite3
import hashlib
import secrets
from groq import Groq
from PIL import Image
from pypdf import PdfReader


st.set_page_config(
    page_title="mobile.app",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

APP = r"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<style>
*{box-sizing:border-box}

:root{
 --mint:#65f5c1;--aqua:#35d8e8;--blue:#668cff;
 --violet:#a77bff;--gold:#ffd477;
 --ink:#102b35;--paper:#f2fff9;--muted:#b9d9d5;
}

html,body{
 margin:0;padding:0;width:100%;min-height:100%;
 font-family:Arial,sans-serif;
 background:linear-gradient(135deg,#c8fff0,#b8d9ff,#e5caff,#fff0c9);
 color:white;
}

body{
 padding:12px 8px 24px;
 background:
 radial-gradient(ellipse at 10% 5%,#70f5cf88,transparent 38%),
 radial-gradient(ellipse at 90% 15%,#8a9dff88,transparent 35%),
 radial-gradient(ellipse at 50% 100%,#ffcf7a66,transparent 42%),
 linear-gradient(135deg,#d7fff1,#d9e7ff 52%,#f1ddff);
}

.phone{
 width:100%;max-width:440px;min-height:820px;
 margin:0 auto;padding:10px;border-radius:38px;
 background:linear-gradient(145deg,#e5fff7,#8be7d3 24%,#92aaff 58%,#d6a9ff 82%,#ffe0a0);
 box-shadow:0 25px 65px #344e7960,inset 0 0 0 2px #ffffffb0;
}

.screen{
 min-height:800px;overflow:hidden;position:relative;
 border-radius:30px;padding:18px 15px 24px;
 background:
 radial-gradient(circle at 5% 0%,#35e9bd55,transparent 35%),
 radial-gradient(circle at 100% 30%,#826bff55,transparent 38%),
 linear-gradient(145deg,#153d49,#173c50 45%,#292c5a 100%);
 border:1px solid #ffffff55;
 transition:background .35s ease;
}

.screen:has(#login-page:not(.hidden)),
.screen:has(#pin-page:not(.hidden)){
 background:radial-gradient(circle at 15% 10%,#40e9c766,transparent 40%),linear-gradient(145deg,#123e4b,#183c61 55%,#44316e);
}
.screen:has(#home-page:not(.hidden)){
 background:radial-gradient(circle at 90% 5%,#ffb75a66,transparent 35%),linear-gradient(145deg,#193b50,#254b67 50%,#51416e);
}
.screen:has(#calculator-page:not(.hidden)){
 background:radial-gradient(circle at 90% 10%,#ffcf6c55,transparent 38%),linear-gradient(145deg,#47304c,#713e55 55%,#a15b55);
}
.screen:has(#password-page:not(.hidden)){
 background:radial-gradient(circle at 90% 5%,#64e7ff55,transparent 38%),linear-gradient(145deg,#123d57,#176b80 55%,#315b83);
}
.screen:has(#notes-page:not(.hidden)){
 background:radial-gradient(circle at 90% 5%,#ffe49a55,transparent 38%),linear-gradient(145deg,#493c2d,#75543c 55%,#986d4d);
}
.screen:has(#games-page:not(.hidden)),
.screen:has(#guess-page:not(.hidden)),
.screen:has(#typing-page:not(.hidden)){
 background:radial-gradient(circle at 90% 5%,#c77bff55,transparent 38%),linear-gradient(145deg,#30265a,#49346e 55%,#743e75);
}
.screen:has(#flappy-page:not(.hidden)){
 background:radial-gradient(circle at 90% 5%,#ffe08b55,transparent 38%),linear-gradient(145deg,#15516c,#267d9b 55%,#55a9a5);
}
.screen:has(#snake-page:not(.hidden)){
 background:radial-gradient(circle at 90% 5%,#a4ff7750,transparent 38%),linear-gradient(145deg,#102f28,#15543d 55%,#28704c);
}
.screen:has(#settings-page:not(.hidden)){
 background:radial-gradient(circle at 90% 5%,#ff9fc855,transparent 38%),linear-gradient(145deg,#482c51,#754267 55%,#a45c70);
}
.screen:has(#about-page:not(.hidden)){
 background:radial-gradient(circle at 90% 5%,#ffe58a55,transparent 38%),linear-gradient(145deg,#51402c,#80603d 55%,#9d8050);
}
.screen:has(#car-page:not(.hidden)){
 background:radial-gradient(circle at 90% 5%,#62f0a855,transparent 38%),linear-gradient(145deg,#102e32,#14564b 55%,#267b62);
}

.topbar{display:flex;justify-content:space-between;align-items:center;color:#eafffa;font-size:12px;margin:2px 4px 20px}
.brand{font-weight:900;letter-spacing:2px;font-size:17px}
.pill{padding:7px 11px;border-radius:30px;background:#ffffff20;border:1px solid #ffffff35;color:#eafffa;font-size:11px}

h1,h2,h3,p{margin-top:0}
h1{font-size:30px;line-height:1.1;margin-bottom:9px}
h2{font-size:21px;margin-bottom:8px}
p{color:#c5e3e2;line-height:1.5;font-size:13px}

button{border:0;cursor:pointer;font-weight:800;font-size:13px;color:#12323a}
.primary{width:100%;padding:15px;border-radius:16px;background:linear-gradient(100deg,var(--mint),var(--aqua),#9bceff);box-shadow:0 8px 22px #36e4ca45}
.secondary{width:100%;padding:14px;border-radius:16px;color:#effffb;background:#ffffff16;border:1px solid #ffffff38}

.login-wrap{min-height:620px;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;padding:4px 5px}
.clock-panel{width:100%;display:flex;align-items:center;justify-content:center;gap:20px;margin:0 auto 16px;padding:15px 12px;border-radius:25px;background:linear-gradient(135deg,#ffffff20,#ffffff09);border:1px solid #ffffff40;box-shadow:0 12px 35px #071b3740}
.login-wrap .clock-panel{transform:translateY(-10px)}
.login-wrap .login-actions{transform:translateY(-10px)}
.clock-face{width:116px;height:116px;position:relative;flex-shrink:0;border-radius:50%;background:radial-gradient(circle at 35% 25%,#fff,#d7fff1 55%,#91d9d0);border:5px solid #f5fffc;box-shadow:0 0 0 5px #70f5c155,0 8px 25px #061b3a70}
.clock-face:before{content:"";position:absolute;inset:8px;border-radius:50%;border:1px solid #7aa9a2}
.clock-face .number{position:absolute;color:#24515a;font-size:10px;font-weight:900;transform:translate(-50%,-50%)}
.hand{position:absolute;left:50%;bottom:50%;transform-origin:50% 100%;border-radius:8px}
.hour-hand{width:5px;height:29px;background:#244c62}
.minute-hand{width:3px;height:39px;background:#287c86}
.second-hand{width:2px;height:43px;background:#ed8b65}
.clock-pin{position:absolute;width:9px;height:9px;border-radius:50%;background:#e89a58;left:50%;top:50%;transform:translate(-50%,-50%)}
.time-info{text-align:left;min-width:0}
.digital-time{font-size:25px;font-weight:900;color:#fff;letter-spacing:1px}
.digital-date{font-size:11px;color:#c9e9e5;margin-top:7px;line-height:1.5}
.login-title{font-size:34px;font-weight:900;letter-spacing:1px;background:linear-gradient(90deg,#a5ffe1,#8ceaff,#d8b4ff,#ffe1a1);-webkit-background-clip:text;background-clip:text;color:transparent}
.login-sub{max-width:290px;margin:6px auto 16px}
.login-actions{width:100%;max-width:310px;display:grid;gap:9px}
.login-actions button{padding-top:16px;padding-bottom:16px}
.section{margin:18px 0}

.card{padding:15px;border-radius:20px;background:linear-gradient(135deg,#ffffff20,#ffffff0c);border:1px solid #ffffff35;box-shadow:0 8px 24px #081b3440}
.tile-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:9px}
.tile{min-height:104px;padding:13px 7px;border-radius:18px;background:linear-gradient(145deg,#176b67,#244b83);border:1px solid #8ce9df;text-align:center;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;color:#f4fffd}
.tile .emoji{font-size:27px}
.tile span:last-child{font-size:11px;font-weight:800}
.wide-tile{width:100%;display:flex;align-items:center;gap:15px;padding:18px;border-radius:20px;text-align:left;color:white;background:linear-gradient(110deg,#a35b27,#b83f70,#6545a6);border:1px solid #ffe0a8;box-shadow:0 10px 25px #081b3440}
.wide-icon{font-size:37px}
.wide-title{font-size:18px;font-weight:900;margin-bottom:5px}
.wide-desc{font-size:11px;color:#effffb;line-height:1.45}
.row-tile{width:100%;display:flex;align-items:center;gap:12px;padding:14px 16px;margin-top:10px;border-radius:16px;text-align:left;color:#f2fffc;background:linear-gradient(110deg,#274d70,#345d57);border:1px solid #91d6c7}
.row-tile .emoji{font-size:22px}
.logout-btn{background:#e53935!important;border-color:#e53935!important;color:#fff!important}
/* COMPACT HOME SHORTCUTS — square neon buttons */
.home-shortcuts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin-top:8px}
.home-shortcut{min-width:0;min-height:78px;padding:8px 4px;border-radius:15px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:5px;text-align:center;color:#f2fffc;background:linear-gradient(145deg,#123b55,#174e55 55%,#382b67);border:1px solid #67f5db88;box-shadow:0 0 12px #42e9d51c,inset 0 0 12px #8cffff0d}
.home-shortcut .emoji{font-size:22px;line-height:1.1}
.home-shortcut b{font-size:10px;line-height:1.2;overflow-wrap:anywhere}
.home-shortcut.neon-shortcut{background:linear-gradient(145deg,#17234d,#38216b);border-color:#a98cff;box-shadow:0 0 13px #9d75ff30}
.home-shortcut.logout-shortcut{background:linear-gradient(145deg,#5b242d,#842e3b);border-color:#ff8c9a}

/* 3D DEPTH FINISH — preserves the existing app background palette */
.phone{box-shadow:0 28px 70px #263d6a70,inset 0 3px 5px #ffffffb8,inset 0 -8px 18px #20345a22}
.screen{box-shadow:inset 0 2px 4px #ffffff30,inset 0 -22px 38px #07142635,0 12px 28px #07142635}
.screen:before{content:"";position:absolute;inset:0;z-index:0;pointer-events:none;border-radius:inherit;background:linear-gradient(145deg,#ffffff0b,transparent 32%,#0000000b 100%);box-shadow:inset 0 1px 0 #ffffff25,inset 0 0 28px #ffffff08}
.screen>*{position:relative;z-index:1}
/* Extra layered depth on the existing pastel background — original colors retained. */
body{background-attachment:fixed;background-image:radial-gradient(ellipse at 12% 12%,#ffffffa8 0,transparent 26%),radial-gradient(ellipse at 88% 18%,#ffffff70 0,transparent 24%),radial-gradient(ellipse at 50% 92%,#ffffff55 0,transparent 32%),radial-gradient(ellipse at 50% 50%,#8bc8ff20 0,transparent 62%),linear-gradient(135deg,#d7fff1,#d9e7ff 52%,#f1ddff)}
.phone{background-image:linear-gradient(145deg,#ffffffa8 0%,#e5fff7 10%,#8be7d3 25%,#92aaff 58%,#d6a9ff 82%,#ffe0a0 100%);box-shadow:0 34px 82px #263d6a75,0 8px 18px #ffffffa0,inset 0 3px 5px #ffffffd0,inset 0 -10px 22px #20345a30}
.screen{background-image:radial-gradient(ellipse at 12% 8%,#ffffff20,transparent 32%),radial-gradient(ellipse at 88% 25%,#8b9dff20,transparent 36%),radial-gradient(ellipse at 50% 100%,#00000018,transparent 48%),radial-gradient(circle at 50% 50%,#ffffff08,transparent 70%),linear-gradient(145deg,#153d49,#173c50 45%,#292c5a 100%)}
button{position:relative;overflow:hidden;transform:translateZ(0);box-shadow:inset 0 2px 0 #ffffff55,inset 0 -4px 0 #00000020,0 7px 14px #06172b38;transition:transform .12s ease,filter .12s ease,box-shadow .12s ease}
button:active{transform:translateY(2px);filter:brightness(.97);box-shadow:inset 0 3px 5px #00000022,0 2px 5px #06172b35}
.card,.clock-panel,.tile,.wide-tile,.row-tile,.home-shortcut,.nb-panel,.school-option,.school-text-card{box-shadow:inset 0 2px 0 #ffffff35,inset 0 -5px 0 #00000018,0 10px 20px #06172b38}
.home-shortcut{border-width:1px 1px 3px}
.home-shortcut:nth-child(1){background:linear-gradient(145deg,#287e91,#164b69);border-color:#8ce9df}
.home-shortcut:nth-child(2){background:linear-gradient(145deg,#7452a8,#39275f);border-color:#c7a6ff}
.home-shortcut:nth-child(3){background:linear-gradient(145deg,#a87836,#654329);border-color:#ffe0a8}
.home-shortcut.neon-shortcut{background:linear-gradient(145deg,#5d42a4,#27214f);border-color:#c4a4ff}
.logout-row{width:100%;min-height:48px;margin-top:9px;padding:10px 15px;border-radius:14px;display:flex;align-items:center;gap:10px;text-align:left;color:#fff;background:linear-gradient(110deg,#a83b43,#702b43);border:1px solid #ff9da5;border-bottom-width:3px}
.logout-row .emoji{font-size:20px}
.logout-row b{font-size:11px;letter-spacing:.6px}
.logout-arrow{margin-left:auto;font-size:22px}
#home-page .section{margin:11px 0}
#home-page .tile{min-height:88px;padding:9px 5px;gap:5px}
#home-page .tile-grid .tile:nth-child(1){background:linear-gradient(145deg,#176b67,#244b83);border-color:#8ce9df}
#home-page .tile-grid .tile:nth-child(2){background:linear-gradient(145deg,#7452a8,#39275f);border-color:#c7a6ff}
#home-page .tile-grid .tile:nth-child(3){background:linear-gradient(145deg,#a87836,#654329);border-color:#ffe0a8}
#home-page .tile .emoji{font-size:23px}
#home-page .wide-tile{padding:12px;gap:10px;border-radius:16px}
#home-page .wide-icon{font-size:29px}
#home-page .wide-title{font-size:15px;margin-bottom:2px}
#home-page .wide-desc{font-size:10px}
/* TWO-SCREEN HOME NAVIGATION + WEATHER FORECAST */
.home-pager{display:flex;width:200%;align-items:flex-start;transition:transform .32s cubic-bezier(.2,.75,.25,1);touch-action:pan-y;will-change:transform}
.home-panel{width:50%;min-width:50%;padding:0 1px}
.home-pagination{display:flex;align-items:center;justify-content:space-between;margin:13px 0 2px;padding:0 8px}
.home-arrow{width:38px;height:34px;border-radius:12px;color:#effffb;background:#ffffff20;border:1px solid #ffffff45;font-size:23px;line-height:1}
.home-dots{display:flex;gap:8px;align-items:center}
.home-dot{width:8px;height:8px;padding:0;border-radius:50%;background:#ffffff55;box-shadow:none}
.home-dot.active{width:22px;border-radius:8px;background:linear-gradient(90deg,#65f5c1,#8dbbff)}
.home-second-heading{display:flex;align-items:center;gap:12px;margin:18px 3px 18px;padding:17px;border-radius:18px;background:linear-gradient(120deg,#ffffff22,#ffffff0c);border:1px solid #ffffff35}
.home-second-heading>span{font-size:31px}.home-second-heading b{display:block;font-size:17px;letter-spacing:1px}.home-second-heading small{display:block;color:#c5e3e2;font-size:10px;margin-top:4px}
.home-shortcuts-second{grid-template-columns:repeat(2,minmax(0,1fr));gap:11px;margin-top:0}
.home-shortcuts-second .home-shortcut{min-height:105px}.home-shortcuts-second .home-shortcut .emoji{font-size:28px}.home-shortcuts-second .home-shortcut b{font-size:11px}
.weather-shortcut{background:linear-gradient(145deg,#176c91,#244a83)!important;border-color:#9be8ff!important}
.home-page-note{text-align:center;color:#c5e3e2;font-size:10px;margin:17px 0 4px}
.weather-hero{padding:16px;border-radius:23px;background:linear-gradient(145deg,#164c70,#246a83 55%,#4d5793);border:1px solid #9ce8f2;box-shadow:inset 0 2px 0 #ffffff35,0 12px 25px #06172b40}
.weather-search{display:flex;gap:7px}.weather-search .field{flex:1;min-width:0;margin:0}.weather-search-btn{padding:0 13px;border-radius:12px;background:linear-gradient(100deg,#65f5c1,#7ddcff);font-size:10px}
.weather-status{font-size:10px;color:#d2f4f2;margin:10px 2px 12px}.weather-current{display:flex;justify-content:space-between;align-items:center;min-height:135px}.weather-place{font-size:19px;font-weight:900}.weather-condition{font-size:12px;color:#d4f4f1;margin-top:4px}.weather-temp{font-size:57px;font-weight:900;line-height:1.15;margin-top:6px}.weather-range{font-size:11px;color:#d2f4f2}.weather-icon{font-size:65px;filter:drop-shadow(0 7px 9px #07172c55)}
.weather-stats{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px;margin-top:13px}.weather-stats>div{padding:9px 5px;border-radius:12px;background:#ffffff17;text-align:center}.weather-stats small{display:block;font-size:8px;color:#d2eeec}.weather-stats b{display:block;font-size:12px;margin-top:5px}
.weather-section{margin-top:18px}.weather-section-title{display:flex;align-items:center;justify-content:space-between}.weather-section-title h3{font-size:16px;margin:0}.weather-section-title span{font-size:9px;letter-spacing:1px;color:#bcece7}.weather-hourly{display:flex;gap:8px;overflow-x:auto;padding:10px 1px 8px;scrollbar-width:thin}.weather-hour{flex:0 0 66px;text-align:center;padding:10px 5px;border-radius:14px;background:#ffffff16;border:1px solid #ffffff20}.weather-hour small{display:block;font-size:10px;color:#d4e9ed}.weather-hour span{display:block;font-size:21px;margin:7px 0}.weather-hour b{font-size:13px}
.weather-daily{display:grid;gap:7px;margin-top:10px}.weather-day{display:grid;grid-template-columns:1fr 30px 45px 45px;align-items:center;gap:7px;padding:10px 11px;border-radius:13px;background:#ffffff14;border:1px solid #ffffff20}.weather-day b{font-size:11px}.weather-day span{font-size:17px;text-align:center}.weather-day small{font-size:10px;color:#d1e8e8;text-align:right}.weather-day strong{font-size:11px;text-align:right}
.weather-error{padding:12px;border-radius:12px;background:#8c303c55;color:#fff;font-size:12px}
@media(max-height:760px){
 #home-page .section{margin:8px 0}
 .home-shortcut{min-height:70px}
}

.page-head{display:flex;align-items:center;gap:12px;margin:6px 0 18px}
.back{padding:10px 13px;border-radius:12px;color:#effffb;background:#ffffff1c;border:1px solid #ffffff35}
.field{width:100%;padding:13px;border-radius:13px;border:1px solid #ffffff55;background:#ffffffed;color:#183a42;font-size:14px;margin:5px 0 12px}
.output{padding:14px;border-radius:14px;background:#ffffffed;color:#183a42;overflow-wrap:anywhere;margin:10px 0}
.calc-display{background:#eafff7;color:#173b42;border-radius:15px;padding:18px;text-align:right;font-size:27px;font-weight:900;min-height:65px;margin-bottom:10px;overflow-wrap:anywhere}
.calc-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:7px}
.calc-key{padding:17px 3px;border-radius:13px;background:#f2fff9;color:#173b42;font-size:16px}
.calc-key.op{background:#ffd477}
.calc-key.equal{background:#65f5c1}
.calc-key.clear{background:#ffb8a8}
.game-canvas{width:100%;display:block;border-radius:17px;background:linear-gradient(#6bd8ff,#b8f1ff);border:2px solid #ffffff55;touch-action:none}
.small-note{font-size:11px;color:#c3e2df}
.hidden{display:none!important}

/* TYPING GAME */
#typing-page .card{padding:14px}
#typing-sentence{padding:14px;border-radius:14px;background:#ffffffed;color:#183a42;font-size:14px;line-height:1.8;min-height:110px}
#typing-input{min-height:105px;resize:vertical}
.typing-stats{display:grid;grid-template-columns:repeat(2,1fr);gap:8px;margin:12px 0}
.typing-stat{padding:12px 8px;border-radius:14px;background:#ffffff18;border:1px solid #ffffff30;text-align:center}
.typing-stat b{display:block;font-size:19px;color:#a5ffe1;margin-bottom:4px}
.typing-stat span{font-size:10px;color:#d6e9ed}
#typing-result{margin-top:10px;white-space:pre-line}

/* SNAKE */
#snake-page{touch-action:none;overscroll-behavior:none}
#snake-page .page-head{margin-bottom:8px}
#snake-page .card{padding:10px;background:linear-gradient(145deg,#ffffff19,#ffffff08);border-color:#aaffbb55}
#snake-page .card>p:first-child{margin-bottom:8px;font-size:11px}
#snake-canvas{width:min(100%,288px);height:auto;aspect-ratio:1/1;margin:0 auto 8px;border-radius:13px;background:linear-gradient(145deg,#092b25,#124c38);border:2px solid #8cffb855;touch-action:none}
#snake-controls{display:grid;grid-template-columns:repeat(3,1fr);gap:6px;max-width:225px;margin:5px auto 8px}
#snake-controls button{min-height:42px;padding:7px;border-radius:12px;font-size:19px;background:linear-gradient(145deg,#d9ffe9,#8af0b7);color:#17432f;box-shadow:0 4px 10px #061b1644}
#snake-controls .empty-control{visibility:hidden}
#snake-page .primary{padding:11px;margin-top:4px}
#snake-page #snake-score{margin:8px 0 0;text-align:center;font-weight:800;color:#c9ffdc}

/* CAR RACING */
#car-page{touch-action:pan-y}
#car-page .card{padding:10px}
#car-canvas{width:100%;max-width:340px;height:auto;display:block;margin:0 auto 10px;border-radius:15px;border:2px solid #ffffff55;background:#245b45;touch-action:none}
.car-controls{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:10px}
.car-controls button{padding:15px;border-radius:15px;background:linear-gradient(145deg,#d9ffe9,#8af0b7);color:#17432f;font-size:20px}
.car-score{display:flex;justify-content:space-between;gap:8px;margin:8px 0}
.car-score div{flex:1;text-align:center;padding:10px 5px;border-radius:12px;background:#ffffff18}
.car-score b{display:block;font-size:18px;color:#b5ffcf}
.car-score span{font-size:10px;color:#e2f8e8}
#car-page .small-note{text-align:center}

@media(max-width:360px){
 body{padding:7px 5px 12px}
 .phone{padding:7px;border-radius:30px}
 .screen{padding:14px 11px 18px;border-radius:24px}
 .clock-panel{gap:12px;padding:15px 8px}
 .clock-face{width:96px;height:96px}
 .digital-time{font-size:20px}
 .tile-grid{gap:7px}
 .tile{min-height:96px}
 #snake-canvas{width:min(100%,260px)}
 #snake-controls{max-width:210px}
 #snake-controls button{min-height:39px}
}

/* ABOUT MY SCHOOL — additions scoped to the new school pages */
.school-page{min-height:760px;border-radius:22px;overflow:hidden;background-image:linear-gradient(180deg,#071d2bc9,#071d2b9c),var(--school-bg);background-size:cover;background-position:center;}
.school-overlay{min-height:760px;padding:16px 12px;background:linear-gradient(180deg,#081b2b55,#081b2b9c)}
.school-menu{display:grid;gap:14px;margin-top:28px}
.school-option{width:100%;display:flex;align-items:center;justify-content:space-between;padding:17px 15px;border-radius:17px;color:white;font-weight:800;text-align:left;border:1px solid #ffffff80;box-shadow:0 8px 22px #06172580}
.school-option span{font-size:23px}
.history-option{background:linear-gradient(110deg,#174d79,#247d83)}
.mission-option{background:linear-gradient(110deg,#80501e,#b17b2e)}
.myself-option{background:linear-gradient(110deg,#563b83,#8b477d)}
.school-detail{min-height:760px;padding:12px;border-radius:22px;}
.history-detail{background:linear-gradient(145deg,#102f49,#176b70)}
.mission-detail{background:linear-gradient(145deg,#3a2c60,#80502e)}
.myself-detail{background:linear-gradient(145deg,#263b67,#613b71)}
.school-text-card{padding:16px;border-radius:18px;background:#fffdf5f5;color:#10232b;line-height:1.75;font-size:16px;font-family:'URW Chancery L','Brush Script MT','Segoe Print',cursive;font-weight:600;text-shadow:0 0 0 transparent}
.school-text-card p{margin:0 0 15px;color:#10232b}
.school-text-card p:last-child{margin-bottom:0}
.school-text-card h3{margin:10px 0 6px;color:#10232b;font-family:'URW Chancery L','Brush Script MT','Segoe Print',cursive;font-size:20px;font-weight:800}
.school-text-card ol{padding-left:24px;margin:8px 0 0;color:#10232b}
.school-text-card li{margin:8px 0;color:#10232b}

/* NEON BREAKOUT — isolated game styles */
#breakout-page{color:#effcff;background:radial-gradient(ellipse at 50% 0%,#183c66 0%,transparent 48%),linear-gradient(160deg,#07101f,#10172c 60%,#17102b);border:1px solid #68eaff35;border-radius:22px;padding:13px;overflow:hidden}
#breakout-page .nb-hero{padding:15px;border:1px solid #72eaff44;border-radius:17px;background:linear-gradient(135deg,#142d49dd,#20163ddd);box-shadow:0 12px 28px #0005}
#breakout-page .nb-kicker{font-size:8px;letter-spacing:.2em;color:#76f5ff;font-weight:900}
#breakout-page h2{color:#f4fbff}#breakout-page h3{font-size:12px;color:#dffaff;margin:15px 2px 8px}
#breakout-page p{font-size:10px;line-height:1.55;color:#a9bfd6}
#breakout-page .nb-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:12px}
#breakout-page .nb-stat{padding:8px 4px;border-radius:11px;background:#ffffff0c;border:1px solid #ffffff18;text-align:center}
#breakout-page .nb-stat b{display:block;font-size:17px;color:#fff}#breakout-page .nb-stat small{font-size:7px;color:#9fc9dc;letter-spacing:.1em}
#breakout-page .nb-panel{padding:11px;border-radius:15px;border:1px solid #78eaff28;background:linear-gradient(145deg,#ffffff12,#ffffff06);margin-top:9px}
#breakout-page canvas{width:100%;display:block;border-radius:13px;border:1px solid #71eaff44;background:#050b19;touch-action:none;box-shadow:0 0 22px #35caff18}
#breakout-page .nb-row{display:flex;gap:7px;flex-wrap:wrap;align-items:center}
#breakout-page .nb-btn{border:1px solid #72eaff66;background:linear-gradient(110deg,#126d8b,#5541a0);color:white;border-radius:10px;padding:10px 12px;font-size:9px;font-weight:900}
#breakout-page .nb-ghost{background:#ffffff0c;border:1px solid #ffffff25;color:#e2f8ff;border-radius:10px;padding:9px 11px;font-size:9px}
#breakout-page .nb-btn:disabled{opacity:.4}
#breakout-page .nb-levels{display:grid;grid-template-columns:repeat(5,1fr);gap:6px}
#breakout-page .nb-level{padding:9px 2px;border:1px solid #6feaff33;background:#ffffff0b;color:#eafaff;border-radius:9px;font-size:9px}
#breakout-page .nb-level.current{background:#1a7790;border-color:#8af5ff;box-shadow:0 0 12px #55eaff55}
#breakout-page .nb-level:disabled{opacity:.3}
#breakout-page .nb-power{padding:8px;border-radius:10px;background:#071526;border:1px solid #ffffff18;margin:5px 0;font-size:9px;color:#b9d6e6}
#breakout-page .nb-power b{color:#fff}
#breakout-page .nb-status{font-size:9px;color:#8df5ff;min-height:16px}


/* FINAL COMPACT GAME LAYOUT — controls remain visible; page scrolling stays enabled. */
#flappy-page .page-head,#snake-page .page-head,#car-page .page-head,#breakout-page .page-head{margin:2px 0 7px;gap:8px}
#flappy-page .card,#snake-page .card,#car-page .card{padding:8px;margin:0}
#flappy-page .card>p:first-child,#snake-page .card>p:first-child,#car-page .card>p:first-child{font-size:10px;line-height:1.25;margin:0 0 5px}
#flappy-canvas{height:clamp(245px,39vh,330px);max-height:330px;width:100%;border-radius:12px;border:1px solid #ffffff55}
#flappy-page .primary{padding:9px 10px;margin-top:6px;font-size:11px}
#flappy-score{margin:5px 0 0;text-align:center;font-size:10px}
#snake-canvas{width:min(100%,min(260px,37vh));max-width:260px;margin:0 auto 5px}
#snake-controls{max-width:195px;gap:4px;margin:3px auto 5px}
#snake-controls button{min-height:34px;padding:4px;font-size:16px}
#snake-page .primary{padding:8px;margin-top:2px;font-size:11px}
#snake-page #snake-score{font-size:10px;margin:4px 0 0}
#car-canvas{height:clamp(245px,39vh,330px);max-height:330px;max-width:310px;margin:0 auto 5px;border-radius:12px}
#car-page .car-score{gap:5px;margin:4px 0}
#car-page .car-score div{padding:5px 3px}
#car-page .car-score b{font-size:14px}
#car-page .car-score span{font-size:8px}
#car-page .car-controls{gap:7px;margin-top:5px}
#car-page .car-controls button{padding:8px;border-radius:11px;font-size:15px}
#car-page .primary{padding:8px;margin-top:6px!important;font-size:11px}
#car-page .small-note{font-size:9px;margin:4px 0 0}
#breakout-page{padding:8px;border-radius:16px}
#breakout-page .nb-hero{padding:8px;border-radius:12px}
#breakout-page .nb-hero h2{font-size:17px!important;margin:3px 0!important}
#breakout-page .nb-hero p{display:none}
#breakout-page .nb-stats{gap:4px;margin-top:5px}
#breakout-page .nb-stat{padding:5px 3px}
#breakout-page .nb-stat b{font-size:13px}
#breakout-page h3{font-size:10px;margin:7px 2px 4px}
#breakout-page .nb-panel{padding:7px;margin-top:5px;border-radius:11px}
#breakout-page canvas{height:clamp(250px,39vh,335px);max-height:335px;width:100%}
#breakout-page .nb-row{gap:5px}
#breakout-page .nb-btn,#breakout-page .nb-ghost{padding:7px 8px;font-size:8px}
#breakout-page .nb-levels{gap:3px}
#breakout-page .nb-level{padding:5px 1px;font-size:8px}
#breakout-page .nb-power{padding:5px;margin:3px 0;font-size:8px}
#games-page .tile-grid{gap:6px}
#games-page .tile{min-height:76px;padding:7px 4px;gap:4px}
#games-page .tile .emoji{font-size:21px}
#games-page .tile span:last-child{font-size:9px}
@media(max-height:700px){
 #flappy-canvas,#car-canvas{height:225px}
 #breakout-page canvas{height:225px}
 #snake-canvas{width:min(220px,31vh)}
}
/* SOLAR SYSTEM EXPLORER */
#solar-page{color:#eef5ff}
.solar-hero{position:relative;overflow:hidden;padding:14px;border:1px solid #ffffff20;border-radius:20px;background:radial-gradient(ellipse at 50% 42%,#172c52 0%,#091326 42%,#030711 78%);box-shadow:inset 0 1px #ffffff16,0 14px 28px #0007}
.solar-kicker{font-size:9px;letter-spacing:2px;color:#8bd9ff;font-weight:800}
.solar-hero h2{font-size:22px;line-height:1.15;margin:8px 0 5px;color:#fff}
.solar-hero>p{font-size:11px;color:#b7c8e4;line-height:1.55;margin:0 0 12px}
.solar-stage{position:relative;width:100%;height:310px;overflow:hidden;border-radius:15px;background:radial-gradient(1px 1px at 8% 16%,#fff 98%,transparent),radial-gradient(1px 1px at 18% 78%,#c6dcff 98%,transparent),radial-gradient(1.5px 1.5px at 32% 28%,#fff 98%,transparent),radial-gradient(1px 1px at 47% 86%,#d7e8ff 98%,transparent),radial-gradient(1px 1px at 61% 13%,#fff 98%,transparent),radial-gradient(1px 1px at 76% 66%,#d8e8ff 98%,transparent),radial-gradient(1px 1px at 92% 31%,#fff 98%,transparent),radial-gradient(ellipse at center,#0c1b35,#030711 72%)}
.solar-system{position:absolute;left:50%;top:50%;width:270px;height:270px;transform:translate(-50%,-50%)}
.solar-sun{position:absolute;left:50%;top:50%;width:48px;height:48px;transform:translate(-50%,-50%);border-radius:50%;z-index:5;overflow:visible;background-color:#ff8a19;background-image:radial-gradient(ellipse at 30% 24%,#fffde2 0%,#fff0a2 8%,transparent 24%),radial-gradient(ellipse at 62% 68%,#ffdb52 0%,#ff9b22 35%,transparent 67%),repeating-conic-gradient(from 12deg at 50% 50%,#ffb12e 0deg 8deg,#ff7b16 9deg 15deg,#ffd34f 16deg 22deg,#f45a12 23deg 29deg),radial-gradient(circle,#fff3a1 0%,#ffb52c 48%,#ed4c0b 78%,#9f2108 100%);background-blend-mode:screen,screen,soft-light,normal;background-size:cover;background-position:center;box-shadow:0 0 13px 5px #ffcf6b,0 0 33px 15px #ff8a2b99,0 0 65px 25px #ff5b1d66,0 0 95px 38px #ff4b1680,inset -5px -4px 9px #8f260b66;animation:sunSurfacePulse 5s ease-in-out infinite alternate}
.solar-sun:before{content:"";position:absolute;inset:3px;border-radius:50%;background:repeating-radial-gradient(ellipse at 38% 42%,#fff3a333 0 1px,#ff7b0b22 2px 3px,transparent 4px 7px),radial-gradient(ellipse at 35% 28%,#fff8c5aa,transparent 42%);mix-blend-mode:screen;opacity:.9;pointer-events:none}
.solar-sun:after{content:"";position:absolute;inset:-7px;border-radius:50%;border:2px solid #ffb52b55;box-shadow:0 0 13px 5px #ff8a2b66;opacity:.75;pointer-events:none}
@keyframes sunSurfacePulse{from{filter:saturate(1.05) brightness(1)}to{filter:saturate(1.28) brightness(1.12)}}
.solar-detail-orb.sun-selected{background-color:#ff8b16!important;background-image:radial-gradient(ellipse at 30% 24%,#fffde2 0%,#fff0a2 8%,transparent 24%),radial-gradient(ellipse at 62% 68%,#ffdb52 0%,#ff9b22 35%,transparent 67%),repeating-conic-gradient(from 12deg at 50% 50%,#ffb12e 0deg 8deg,#ff7b16 9deg 15deg,#ffd34f 16deg 22deg,#f45a12 23deg 29deg),radial-gradient(circle,#fff3a1 0%,#ffb52c 48%,#ed4c0b 78%,#9f2108 100%)!important;background-blend-mode:screen,screen,soft-light,normal!important;box-shadow:0 0 18px 5px #ffb13b99,0 0 42px 12px #ff7b2e99,0 0 68px 20px #ff4b1677!important;animation:sunSurfacePulse 5s ease-in-out infinite alternate}
.solar-orbit{position:absolute;left:50%;top:50%;border:1px solid #8bb5e52c;border-radius:50%;transform:translate(-50%,-50%);animation:solarOrbit linear infinite}
.solar-orbit .solar-body{position:absolute;left:50%;top:0;border-radius:50%;transform:translate(-50%,-50%);box-shadow:0 0 9px #ffffff55}
.solar-orbit.o1{width:54px;height:54px;animation-duration:5s}.solar-orbit.o2{width:78px;height:78px;animation-duration:8s}.solar-orbit.o3{width:105px;height:105px;animation-duration:12s}.solar-orbit.o4{width:132px;height:132px;animation-duration:18s}.solar-orbit.o5{width:174px;height:174px;animation-duration:28s}.solar-orbit.o6{width:213px;height:213px;animation-duration:38s}.solar-orbit.o7{width:246px;height:246px;animation-duration:48s}.solar-orbit.o8{width:276px;height:276px;animation-duration:60s}
.solar-orbit .solar-body{background-size:cover;background-position:center;box-shadow:inset -3px -2px 5px #000b,0 0 8px #ffffff66}
.solar-orbit.o1 .solar-body{width:6px;height:6px;background-image:url("https://www.solarsystemscope.com/textures/download/2k_mercury.jpg")}
.solar-orbit.o2 .solar-body{width:8px;height:8px;background-image:url("https://www.solarsystemscope.com/textures/download/2k_venus_surface.jpg")}
.solar-orbit.o3 .solar-body{width:10px;height:10px;background-image:url("https://www.solarsystemscope.com/textures/download/2k_earth_daymap.jpg")}
.solar-orbit.o4 .solar-body{width:8px;height:8px;background-image:url("https://www.solarsystemscope.com/textures/download/2k_mars.jpg")}
.solar-orbit.o5 .solar-body{width:18px;height:18px;background-image:url("https://www.solarsystemscope.com/textures/download/2k_jupiter.jpg")}
.solar-orbit.o6 .solar-body{width:16px;height:16px;background-image:url("https://www.solarsystemscope.com/textures/download/2k_saturn.jpg");outline:2px solid #d9c18a88;outline-offset:2px}
.solar-orbit.o7 .solar-body{width:12px;height:12px;background-image:url("https://www.solarsystemscope.com/textures/download/2k_uranus.jpg")}
.solar-orbit.o8 .solar-body{width:11px;height:11px;background-image:url("https://www.solarsystemscope.com/textures/download/2k_neptune.jpg")}
.solar-orbit.o6 .solar-body:after{content:"";position:absolute;left:50%;top:50%;width:185%;height:48%;border:1px solid #d8c28a99;border-radius:50%;transform:translate(-50%,-50%) rotate(-18deg);pointer-events:none}
@keyframes solarOrbit{from{transform:translate(-50%,-50%) rotate(0)}to{transform:translate(-50%,-50%) rotate(360deg)}}
.solar-stage-label{position:absolute;left:10px;bottom:9px;font-size:8px;letter-spacing:1px;color:#8fa9cb}
.solar-toolbar{display:flex;gap:7px;flex-wrap:wrap;margin:10px 0}.solar-tool{border:1px solid #4d759d;background:linear-gradient(135deg,#183b60,#152847);color:#eaf5ff;border-radius:10px;padding:9px 11px;font-size:10px;font-weight:800}.solar-tool.active{border-color:#6fe0d3;background:linear-gradient(135deg,#075d61,#174c73)}
.solar-planet-list{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:7px;margin:12px 0}.solar-pick{min-width:0;padding:9px 4px;border:1px solid #ffffff20;border-radius:12px;background:#101d32;color:#e8f1ff;font-size:10px;font-weight:800}.solar-pick .dot{display:block;width:19px;height:19px;border-radius:50%;margin:0 auto 6px;box-shadow:0 0 9px #ffffff44}.solar-pick.selected{border-color:#69e6d1;background:linear-gradient(145deg,#124c59,#172d50);box-shadow:0 0 0 1px #69e6d144}

.solar-pick .dot{background-size:cover!important;background-position:center!important;box-shadow:inset -3px -2px 5px #000a,0 0 9px #ffffff55!important}
#solar-pick-mercury .dot{background-image:url("https://www.solarsystemscope.com/textures/download/2k_mercury.jpg")!important}
#solar-pick-venus .dot{background-image:url("https://www.solarsystemscope.com/textures/download/2k_venus_surface.jpg")!important}
#solar-pick-earth .dot{background-image:url("https://www.solarsystemscope.com/textures/download/2k_earth_daymap.jpg")!important}
#solar-pick-mars .dot{background-image:url("https://www.solarsystemscope.com/textures/download/2k_mars.jpg")!important}
#solar-pick-jupiter .dot{background-image:url("https://www.solarsystemscope.com/textures/download/2k_jupiter.jpg")!important}
#solar-pick-saturn .dot{background-image:url("https://www.solarsystemscope.com/textures/download/2k_saturn.jpg")!important}
#solar-pick-uranus .dot{background-image:url("https://www.solarsystemscope.com/textures/download/2k_uranus.jpg")!important}
#solar-pick-neptune .dot{background-image:url("https://www.solarsystemscope.com/textures/download/2k_neptune.jpg")!important}
.solar-detail-orb{background-size:cover;background-position:center;box-shadow:inset -11px -8px 15px #000b,0 0 18px #ffffff35}
.solar-detail-orb.sun-selected{box-shadow:0 0 18px 5px #ffb13b99,0 0 42px 12px #ff7b2e66,inset -8px -6px 12px #65160099}
.solar-detail{padding:13px;border:1px solid #ffffff20;border-radius:17px;background:linear-gradient(145deg,#101f38,#0a1425);margin-top:10px}.solar-detail-top{display:flex;align-items:center;gap:11px}.solar-detail-orb{width:53px;height:53px;flex:0 0 53px;border-radius:50%;box-shadow:inset -9px -7px 14px #0009,0 0 18px #ffffff25}.solar-detail h3{margin:0;font-size:19px;color:#fff}.solar-detail small{font-size:9px;color:#9db6d6;letter-spacing:1px}.solar-detail p{font-size:11px;line-height:1.65;color:#c7d5e9;margin:10px 0}.solar-facts{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}.solar-fact{padding:9px;border-radius:10px;background:#ffffff09;border:1px solid #ffffff12}.solar-fact b{display:block;font-size:12px;color:#fff}.solar-fact span{font-size:8px;color:#9db6d6;letter-spacing:.7px}.solar-section-title{font-size:13px;color:#eaf4ff;margin:15px 0 8px}.solar-moon-list{display:flex;flex-wrap:wrap;gap:6px}.solar-moon-chip{font-size:9px;padding:6px 8px;border-radius:20px;background:#21324b;border:1px solid #5c789b;color:#d9e9ff}.solar-note{font-size:9px;color:#91a8c6;line-height:1.55;margin:9px 2px 0}
@media(max-width:370px){.solar-stage{height:285px}.solar-system{transform:translate(-50%,-50%) scale(.88)}.solar-planet-list{gap:5px}.solar-pick{font-size:9px}}
@media(prefers-reduced-motion:reduce){.solar-orbit{animation-play-state:paused!important}}

/* Planet texture fallback gradients keep every world visible if remote textures fail. */
.solar-orbit.o1 .solar-body{background-image:radial-gradient(circle at 28% 24%,#f4eee2 0%,#aaa39a 38%,#55545a 72%,#252832 100%),url("https://www.solarsystemscope.com/textures/download/2k_mercury.jpg")}
.solar-orbit.o2 .solar-body{background-image:radial-gradient(circle at 28% 24%,#fff0bf 0%,#d6a15d 45%,#8e5935 78%,#38251f 100%),url("https://www.solarsystemscope.com/textures/download/2k_venus_surface.jpg")}
.solar-orbit.o3 .solar-body{background-image:radial-gradient(circle at 28% 24%,#baf4ff 0%,#268ed0 43%,#17603c 62%,#071d55 100%),url("https://www.solarsystemscope.com/textures/download/2k_earth_daymap.jpg")}
.solar-orbit.o4 .solar-body{background-image:radial-gradient(circle at 28% 24%,#ffd4a2 0%,#c65d37 48%,#743323 78%,#291b20 100%),url("https://www.solarsystemscope.com/textures/download/2k_mars.jpg")}
.solar-orbit.o5 .solar-body{background-image:repeating-linear-gradient(8deg,#e9c9a2 0 3px,#a96f4f 4px 6px,#f2dfbf 7px 9px),url("https://www.solarsystemscope.com/textures/download/2k_jupiter.jpg")}
.solar-orbit.o6 .solar-body{background-image:radial-gradient(circle at 28% 24%,#fff2cb 0%,#d3b17c 48%,#8d6b48 80%,#3a3029 100%),url("https://www.solarsystemscope.com/textures/download/2k_saturn.jpg")}
.solar-orbit.o7 .solar-body{background-image:radial-gradient(circle at 28% 24%,#e0ffff 0%,#91dce0 48%,#478eaa 80%,#1b3d59 100%),url("https://www.solarsystemscope.com/textures/download/2k_uranus.jpg")}
.solar-orbit.o8 .solar-body{background-image:radial-gradient(circle at 28% 24%,#b9dcff 0%,#426fce 48%,#203b91 80%,#101d52 100%),url("https://www.solarsystemscope.com/textures/download/2k_neptune.jpg")}
#solar-pick-mercury .dot{background-image:radial-gradient(circle at 28% 24%,#f4eee2 0%,#aaa39a 38%,#55545a 72%,#252832 100%),url("https://www.solarsystemscope.com/textures/download/2k_mercury.jpg")!important}
#solar-pick-venus .dot{background-image:radial-gradient(circle at 28% 24%,#fff0bf 0%,#d6a15d 45%,#8e5935 78%,#38251f 100%),url("https://www.solarsystemscope.com/textures/download/2k_venus_surface.jpg")!important}
#solar-pick-earth .dot{background-image:radial-gradient(circle at 28% 24%,#baf4ff 0%,#268ed0 43%,#17603c 62%,#071d55 100%),url("https://www.solarsystemscope.com/textures/download/2k_earth_daymap.jpg")!important}
#solar-pick-mars .dot{background-image:radial-gradient(circle at 28% 24%,#ffd4a2 0%,#c65d37 48%,#743323 78%,#291b20 100%),url("https://www.solarsystemscope.com/textures/download/2k_mars.jpg")!important}
#solar-pick-jupiter .dot{background-image:repeating-linear-gradient(8deg,#e9c9a2 0 3px,#a96f4f 4px 6px,#f2dfbf 7px 9px),url("https://www.solarsystemscope.com/textures/download/2k_jupiter.jpg")!important}
#solar-pick-saturn .dot{background-image:radial-gradient(circle at 28% 24%,#fff2cb 0%,#d3b17c 48%,#8d6b48 80%,#3a3029 100%),url("https://www.solarsystemscope.com/textures/download/2k_saturn.jpg")!important}
#solar-pick-uranus .dot{background-image:radial-gradient(circle at 28% 24%,#e0ffff 0%,#91dce0 48%,#478eaa 80%,#1b3d59 100%),url("https://www.solarsystemscope.com/textures/download/2k_uranus.jpg")!important}
#solar-pick-neptune .dot{background-image:radial-gradient(circle at 28% 24%,#b9dcff 0%,#426fce 48%,#203b91 80%,#101d52 100%),url("https://www.solarsystemscope.com/textures/download/2k_neptune.jpg")!important}
.solar-stage{height:285px}

/* END SOLAR SYSTEM EXPLORER */

/* QURAN READER — added feature */
#quran-page .quran-panel{padding:13px;border-radius:17px;background:linear-gradient(145deg,#ffffff20,#ffffff0c);border:1px solid #ffffff35;margin:10px 0}
#quran-page .quran-control{width:100%;padding:11px;border-radius:12px;border:1px solid #ffffff55;background:#f5fffc;color:#173b42;font-size:13px;margin:5px 0 10px}
#quran-page label{display:block;font-size:11px;color:#d9f4ed;font-weight:800;margin-top:5px}
#quran-page .quran-arabic{font-family:'Amiri','Scheherazade New','Noto Naskh Arabic',serif;direction:rtl;text-align:right;font-size:2rem;line-height:1.65;margin:15px 0;color:#fff;overflow-wrap:anywhere}
#quran-page .quran-translation{font-size:13px;line-height:1.7;color:#e1f0ec;margin:7px 0 15px}
#quran-page .quran-bismillah{text-align:center;font-family:'Amiri','Noto Naskh Arabic',serif;font-size:1.8rem;line-height:1.8;margin:15px 0;color:#fff}
#quran-page .quran-ayah{padding:10px 0;border-bottom:1px solid #ffffff25}
#quran-page .quran-ayah audio{width:100%;height:36px;margin:5px 0}
#quran-page .quran-meta{font-size:11px;color:#c4e4dd;line-height:1.6}
#quran-page .quran-status{font-size:12px;color:#cffff0;min-height:20px;margin:7px 0}
#quran-page .quran-range{width:100%;accent-color:#65f5c1;margin:8px 0 12px}




/* REQUESTED DESIGN UPDATE: three-tone premium palette, wider phone and compact spacing. */
body{background-attachment:fixed;background-image:radial-gradient(ellipse at 12% 8%,#79f3d755,transparent 32%),radial-gradient(ellipse at 88% 20%,#a58aff55,transparent 34%),radial-gradient(ellipse at 50% 100%,#ff927b40,transparent 38%),linear-gradient(135deg,#071d28 0%,#123e48 48%,#34254f 100%)}
.phone{background:linear-gradient(135deg,#8ff5d7 0%,#8ba8ff 52%,#ffb18f 100%);}
.screen{padding:12px 13px 18px;background:radial-gradient(circle at 8% 0%,#39e9bd45,transparent 34%),radial-gradient(circle at 95% 28%,#a47bff45,transparent 38%),linear-gradient(145deg,#102d3a 0%,#174653 52%,#30264f 100%)}
.dynamic-island{width:92px;height:23px;margin:0 auto 8px;border-radius:20px;background:linear-gradient(110deg,#020509,#10151b);border:1px solid #52606b88;box-shadow:inset 0 1px 3px #ffffff22,0 2px 8px #0006;display:flex;align-items:center;justify-content:flex-end;padding:0 10px;position:relative;z-index:3}
.dynamic-island span{width:7px;height:7px;border-radius:50%;background:#172b3d;box-shadow:inset 0 0 3px #65a6d8,0 0 4px #4c8ecb;margin-right:2px}
.dynamic-island i{width:5px;height:5px;border-radius:50%;background:#172d3b;box-shadow:0 0 3px #3c8bba}
.topbar{margin:0 4px 13px}
.section{margin:12px 0}
.card{padding:12px}
.page-head{margin:3px 0 12px}
.tile{min-height:84px;padding:9px 6px}
@media(max-width:480px){.phone{max-width:100%;padding:7px;border-radius:30px}.screen{padding:10px 11px 16px;border-radius:24px}.dynamic-island{height:21px;width:86px;margin-bottom:7px}}

.screen:has(#games-page:not(.hidden)){background:radial-gradient(circle at 8% 5%,#55e6d055,transparent 35%),radial-gradient(circle at 92% 20%,#b07bff55,transparent 38%),linear-gradient(145deg,#172b50,#34265e 55%,#743d68)}
.screen:has(#solar-page:not(.hidden)){background:radial-gradient(circle at 10% 5%,#54d9d955,transparent 35%),radial-gradient(circle at 92% 20%,#8c83ff55,transparent 38%),linear-gradient(145deg,#071a30,#142d50 55%,#34264e)}
.screen:has(#house-page:not(.hidden)){background:radial-gradient(circle at 8% 5%,#e7bd8055,transparent 35%),radial-gradient(circle at 92% 20%,#93c7d955,transparent 38%),linear-gradient(145deg,#253849,#425166 55%,#68475a)}
.screen:has(#quran-page:not(.hidden)){background:radial-gradient(circle at 8% 5%,#65e9bd55,transparent 35%),radial-gradient(circle at 92% 20%,#e0b36b44,transparent 38%),linear-gradient(145deg,#123c43,#18565a 55%,#3d3458)}
.screen:has(#typing-page:not(.hidden)){background:radial-gradient(circle at 8% 5%,#6ae6d355,transparent 35%),radial-gradient(circle at 92% 20%,#ff9cbb44,transparent 38%),linear-gradient(145deg,#302653,#55335f 55%,#78465b)}


/* SECTION-SPECIFIC COLOUR THEMES — individual colour mixes for each screen. */
.screen:has(#app-login-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#ff6f9160,transparent 34%),radial-gradient(circle at 92% 18%,#63b8ff55,transparent 36%),linear-gradient(145deg,#301c43,#63304f 54%,#173c5a)}
.screen:has(#guess-page:not(.hidden)){background:radial-gradient(circle at 10% 8%,#ffce5b55,transparent 34%),radial-gradient(circle at 92% 18%,#ff718755,transparent 36%),linear-gradient(145deg,#4b2a3c,#78452e 55%,#34305c)}
.screen:has(#flappy-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#ffe66d66,transparent 34%),radial-gradient(circle at 92% 18%,#55e5e055,transparent 36%),linear-gradient(145deg,#15516d,#258b9a 55%,#3e668d)}
.screen:has(#snake-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#a5ff7655,transparent 34%),radial-gradient(circle at 92% 18%,#58d9ff44,transparent 36%),linear-gradient(145deg,#123b31,#17634b 55%,#244c70)}
.screen:has(#car-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#ffcc5b55,transparent 34%),radial-gradient(circle at 92% 18%,#ff758a44,transparent 36%),linear-gradient(145deg,#422c38,#795039 55%,#35476c)}
.screen:has(#settings-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#ff9bc855,transparent 34%),radial-gradient(circle at 92% 18%,#8e9aff55,transparent 36%),linear-gradient(145deg,#46294e,#75416a 55%,#38446f)}
.screen:has(#about-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#ffe27a55,transparent 34%),radial-gradient(circle at 92% 18%,#ff9d7350,transparent 36%),linear-gradient(145deg,#51402c,#86543e 55%,#54416e)}
.screen:has(#school-page:not(.hidden)),.screen:has(#school-history-page:not(.hidden)),.screen:has(#school-mission-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#69dfff55,transparent 34%),radial-gradient(circle at 92% 18%,#ffd46a44,transparent 36%),linear-gradient(145deg,#173d60,#285b69 55%,#55406c)}
.screen:has(#password-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#61e9ff55,transparent 34%),radial-gradient(circle at 92% 18%,#b28cff44,transparent 36%),linear-gradient(145deg,#153d5b,#176c78 55%,#3b477a)}
.screen:has(#notes-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#ffe17c55,transparent 34%),radial-gradient(circle at 92% 18%,#ff9e7c44,transparent 36%),linear-gradient(145deg,#51402e,#80583e 55%,#5b4569)}
.screen:has(#shopping-page:not(.hidden)){background:radial-gradient(circle at 8% 5%,#ff6d8c55,transparent 35%),radial-gradient(circle at 92% 18%,#69baff55,transparent 36%),radial-gradient(circle at 50% 100%,#ffe06a33,transparent 40%),linear-gradient(145deg,#271f42,#3e315c 52%,#174e60)}
.shop-hero{padding:13px;border-radius:18px;background:linear-gradient(130deg,#ffffff20,#ffffff08);border:1px solid #ffffff35;box-shadow:0 8px 20px #07172d30}.shop-kicker{font-size:8px;letter-spacing:2px;font-weight:900;color:#ffd88b}.shop-hero h2{font-size:21px;margin:6px 0;color:#fff}.shop-hero p{font-size:10px;margin:0 0 8px}.shop-search-row{display:flex;gap:7px;align-items:center}.shop-search-row .field{margin:0;min-width:0;padding:10px;font-size:12px;flex:1}.shop-cart-button{min-width:58px;padding:11px 8px;border-radius:12px;color:#fff;background:linear-gradient(135deg,#e65b7b,#8c4ac1);border:1px solid #ffffff66}.shop-categories{display:flex;gap:6px;overflow-x:auto;padding:10px 0 5px;scrollbar-width:none}.shop-categories::-webkit-scrollbar{display:none}.shop-category{white-space:nowrap;padding:8px 10px;border-radius:20px;color:#f5f4ff;background:#ffffff16;border:1px solid #ffffff35;font-size:9px}.shop-category.active{background:linear-gradient(110deg,#ff718b,#8c6bff);border-color:#ffd1df;color:#fff}.shop-section-head{display:flex;align-items:center;justify-content:space-between;margin:8px 1px}.shop-section-head h3{font-size:14px;margin:0;color:#fff}.shop-section-head span{font-size:9px;color:#d7d8ef}.shop-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px}.shop-product{min-width:0;padding:8px;border-radius:15px;background:linear-gradient(145deg,#ffffff20,#ffffff0b);border:1px solid #ffffff35;box-shadow:0 6px 14px #07172d30;contain:layout paint}.shop-product-art{height:92px;border-radius:11px;display:flex;align-items:center;justify-content:center;font-size:43px;background:linear-gradient(135deg,#ffbd8a,#e77d9f 48%,#8679d9);margin-bottom:7px}.shop-product:nth-child(4n+2) .shop-product-art{background:linear-gradient(135deg,#77d8d1,#6e9ee7,#aa83dc)}.shop-product:nth-child(4n+3) .shop-product-art{background:linear-gradient(135deg,#ffe18c,#e9a36f,#dc7e9e)}.shop-product:nth-child(4n+4) .shop-product-art{background:linear-gradient(135deg,#8ce6aa,#5ca9a9,#6c82cf)}.shop-product h4{font-size:11px;line-height:1.25;margin:4px 0;color:#fff;min-height:27px}.shop-product .shop-category-name{font-size:8px;color:#d5d9f0}.shop-product .shop-price{font-size:12px;font-weight:900;color:#ffe39a;margin:5px 0}.shop-product .shop-old-price{font-size:8px;color:#d2cde0;text-decoration:line-through;margin-left:4px}.shop-add{width:100%;padding:8px 5px;border-radius:9px;background:linear-gradient(100deg,#64e5c1,#73b9ff);font-size:9px}.shop-cart-panel{margin-top:12px;padding:12px;border-radius:16px;background:linear-gradient(145deg,#172a4b,#4c315c);border:1px solid #ffffff55}.shop-cart-head{display:flex;justify-content:space-between;align-items:center}.shop-cart-head h3{font-size:15px;margin:0 0 8px}.shop-close{background:#ffffff20;color:white;border-radius:8px;padding:6px 9px}.shop-cart-line{display:flex;align-items:center;gap:8px;padding:8px 0;border-bottom:1px solid #ffffff20;font-size:10px}.shop-cart-line span:nth-child(2){flex:1}.shop-cart-line button{padding:4px 7px;border-radius:7px;background:#ffffff20;color:white}.shop-total{display:flex;justify-content:space-between;padding:12px 0;color:#fff;font-size:12px}.shop-total b{color:#ffe39a}.shop-message{font-size:11px;color:#c8ffe9;min-height:15px;margin:7px 0}.shop-shortcut{background:linear-gradient(145deg,#bd4e78,#7044a6)!important;border-color:#ffc0dc!important}
@media(max-width:360px){.shop-product-art{height:78px}.shop-grid{gap:6px}.shop-product{padding:6px}}
/* Pause off-screen orbital motion to reduce background CPU use on phones. */
.screen:has(#solar-page.hidden) .solar-orbit{animation-play-state:paused!important}


/* MOBILE FIT + UPDATED RED / WARM ACCENT PALETTE */
#home-page{width:100%;max-width:100%;overflow:hidden;position:relative;isolation:isolate}
#home-page>.home-pager{width:200%;max-width:none;overflow:visible;flex-wrap:nowrap}
#home-page .home-panel{flex:0 0 50%;width:50%;min-width:50%;max-width:50%}
.screen:has(#home-page:not(.hidden)){
 background:
 radial-gradient(ellipse at 92% 8%,#ff526b55,transparent 34%),
 radial-gradient(ellipse at 8% 78%,#b64b7850,transparent 38%),
 linear-gradient(145deg,#182c48 0%,#382b50 48%,#612f49 100%);
}
body{background:
 radial-gradient(ellipse at 12% 12%,#ff657533,transparent 28%),
 radial-gradient(ellipse at 88% 18%,#b46cff35,transparent 26%),
 linear-gradient(135deg,#171e36,#39283f 55%,#512d3d)!important}
.phone{background:linear-gradient(145deg,#ffe0e5 0%,#d86a7d 24%,#7861a9 58%,#393b67 100%)!important}
.screen{background:
 radial-gradient(ellipse at 12% 8%,#ff75851e,transparent 32%),
 radial-gradient(ellipse at 88% 25%,#a88bff20,transparent 36%),
 linear-gradient(145deg,#172b43,#27334f 48%,#472b46 100%)!important}
.weather-hero{
 background:radial-gradient(circle at 90% 5%,#ff9b6c55,transparent 38%),
 linear-gradient(145deg,#422b50,#71364e 58%,#34456e);
 border-color:#ffb1a9;
 box-shadow:inset 0 2px 0 #ffffff42,0 14px 28px #06172b55
}
.weather-search-btn{background:linear-gradient(110deg,#ff6b70,#ffad70);color:#fff;border:1px solid #ffd0b8}
.weather-stats>div{background:linear-gradient(145deg,#ffffff22,#ffffff0b);border:1px solid #ffffff22}
.weather-stats b{color:#ffe0bd}
.weather-section{padding:12px;border-radius:17px;background:linear-gradient(145deg,#ffffff12,#ffffff06);border:1px solid #ffffff20}
.weather-section-title span{color:#ffc2bd}
.weather-hour{background:linear-gradient(160deg,#ffffff20,#ffffff09);border-color:#ffffff30}
.weather-day{background:linear-gradient(110deg,#ffffff1c,#ffffff08);border-color:#ffffff2b}
.weather-extra-stats{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:7px;margin-top:9px}
.weather-extra-stats>div{padding:10px 6px;border-radius:13px;text-align:center;background:#ffffff16;border:1px solid #ffffff24}
.weather-extra-stats small{display:block;font-size:8px;color:#f2dce3}
.weather-extra-stats b{display:block;font-size:11px;margin-top:5px;color:#fff0dc}
.weather-kicker{font-size:9px;letter-spacing:1.8px;font-weight:900;color:#ffc1a9;margin:0 0 5px}
.weather-place{font-size:20px}
.weather-status{color:#f4dfe5}
.weather-temp{text-shadow:0 5px 18px #160c2d66}


/* GENTLE MOBILE FIT: slightly roomier controls, only a little page scroll */
@media(max-width:480px){
 body{padding:7px 4px 12px}
 .phone{max-width:440px;min-height:0;padding:8px;border-radius:30px}
 .screen{min-height:0;padding:15px 12px 17px;border-radius:25px}
 .topbar{margin:0 4px 13px}
 #home-page .section{margin:9px 0}
 #home-page .section:first-child p{font-size:10.5px;margin-bottom:3px}
 #home-page .section:first-child h1{font-size:26px;margin:3px 0 4px}
 #home-page .section:first-child p:last-child{font-size:10.5px;margin-bottom:1px}
 #home-page .tile-grid{gap:8px}
 #home-page .tile{min-height:82px;padding:9px 6px;gap:5px;border-radius:15px}
 #home-page .tile .emoji{font-size:24px}
 #home-page .tile span:last-child{font-size:11px}
 #home-page .wide-tile{padding:11px 12px;gap:10px;border-radius:15px}
 #home-page .wide-icon{font-size:28px}
 #home-page .wide-title{font-size:15px}
 #home-page .wide-desc{font-size:10px;line-height:1.3}
 #home-page .home-shortcuts{gap:8px;margin-top:8px}
 #home-page .home-shortcut{min-height:72px;padding:8px 5px;gap:5px;border-radius:14px}
 #home-page .home-shortcut .emoji{font-size:22px}
 #home-page .home-shortcut b{font-size:9px;line-height:1.18}
 #home-page .home-shortcuts-second{gap:8px}
 #home-page .home-shortcuts-second .home-shortcut{min-height:84px}
 #home-page .home-shortcuts-second .home-shortcut .emoji{font-size:24px}
 #home-page .home-shortcuts-second .home-shortcut b{font-size:10px}
 #home-page .home-second-heading{margin:10px 3px 10px;padding:11px;border-radius:15px}
 #home-page .home-second-heading>span{font-size:25px}
 #home-page .home-second-heading b{font-size:14.5px}
 #home-page .home-second-heading small{font-size:9.5px}
 #home-page .home-page-note{font-size:9.5px;margin:9px 0 3px}
 #home-page .logout-row{min-height:42px;margin-top:8px;padding:8px 12px;border-radius:12px}
 #home-page .logout-row .emoji{font-size:17px}
 #home-page .home-pagination{margin:9px 0 0;padding:0 6px}
 #home-page .home-arrow{width:34px;height:31px;font-size:21px}
}


/* Restore the original centered smartphone frame; do not stretch it to the browser. */
html,body{width:100%!important;min-width:0!important;overflow-x:hidden!important}
body{padding:12px 8px 24px!important}
.phone{width:100%!important;max-width:440px!important;min-height:820px!important;height:auto!important;margin:0 auto!important;padding:10px!important;border:0!important;border-radius:38px!important;box-shadow:0 25px 65px #344e7960,inset 0 0 0 2px #ffffffb0!important}
.screen{width:100%!important;max-width:100%!important;min-height:800px!important;height:auto!important;margin:0!important;padding:12px 13px 18px!important;border:1px solid #ffffff55!important;border-radius:30px!important;overflow:hidden!important;box-shadow:none!important}
@media(max-width:480px){body{padding:8px 5px 18px!important}.phone{max-width:440px!important;padding:7px!important;border-radius:30px!important}.screen{padding:10px 11px 16px!important;border-radius:24px!important}}

/* Product detail interaction */
.shop-product{cursor:pointer;transition:transform .16s ease,border-color .16s ease}
.shop-product:active{transform:scale(.975)}
.shop-detail{position:relative;margin:10px 0;padding:14px;border-radius:17px;background:linear-gradient(145deg,#182d50,#57365e);border:1px solid #ffffff55;color:#fff;box-shadow:0 12px 28px #07172d55}
.shop-detail-art{height:130px;display:flex;align-items:center;justify-content:center;font-size:68px;border-radius:13px;background:linear-gradient(135deg,#ffbd8a,#e77d9f 48%,#8679d9);margin:8px 0 12px}
.shop-detail h3{font-size:17px;margin:5px 0}.shop-detail p{font-size:11px;line-height:1.5;color:#e4e5f6}
.shop-detail-actions{display:flex;gap:8px}.shop-detail-actions button{flex:1;padding:10px 6px;border-radius:10px;font-size:10px;font-weight:900}
.shop-detail-add{background:linear-gradient(100deg,#64e5c1,#73b9ff);color:#10263b}.shop-detail-buy{background:linear-gradient(100deg,#ffd477,#ff9d8a);color:#3c2330}.shop-detail-close{position:absolute;right:10px;top:10px;border-radius:8px;padding:5px 9px;background:#ffffff22;color:#fff}


/* HOUSE DESIGNER — isolated responsive floor-plan studio */
#house-page{color:#f4fbff}
.hd-hero{padding:15px;border-radius:19px;background:radial-gradient(circle at 90% 0%,#e7b56b44,transparent 40%),linear-gradient(140deg,#183b4d,#34405d 60%,#68415c);border:1px solid #f0d0a766;box-shadow:0 12px 25px #07172b55}
.hd-kicker{font-size:8px;letter-spacing:2px;color:#ffdc9c;font-weight:900}.hd-hero h2{font-size:22px;margin:7px 0 5px;color:#fff}.hd-hero p{font-size:10px;color:#d9e7ed;line-height:1.5;margin:0}.hd-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:7px;margin-top:13px}.hd-stats div{padding:8px 4px;border-radius:11px;background:#ffffff12;border:1px solid #ffffff20;text-align:center}.hd-stats b{display:block;font-size:18px;color:#ffe1a8}.hd-stats span{font-size:7px;letter-spacing:1px;color:#d5e5ed}
.hd-toolbar{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin:10px 0}.hd-tab{padding:11px 5px;border-radius:11px;background:#ffffff12;border:1px solid #ffffff30;color:#eaf8ff;font-size:9px}.hd-tab.active{background:linear-gradient(110deg,#d8a66b,#f1d6a0);border-color:#ffe6b6;color:#342b2a}.hd-canvas-wrap{position:relative;padding:7px;border-radius:16px;background:linear-gradient(145deg,#101c2c,#25364a);border:1px solid #ffffff35;box-shadow:inset 0 1px #ffffff20,0 12px 25px #06172b55}.hd-canvas-wrap canvas{width:100%;height:auto;display:block;border-radius:10px;background:#e9e2d4;touch-action:none}.hd-canvas-hint{font-size:8px;color:#c5d8e5;text-align:center;padding:7px 2px 1px}.hd-controls{display:grid;gap:9px;margin-top:10px}.hd-panel{padding:11px;border-radius:15px;background:linear-gradient(145deg,#ffffff18,#ffffff09);border:1px solid #ffffff28;box-shadow:inset 0 1px #ffffff20,0 8px 18px #06172b30}.hd-panel-head{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:9px}.hd-panel-head h3{font-size:13px;margin:0;color:#fff}.hd-panel-head span{font-size:7px;letter-spacing:1px;color:#f3d29d}.hd-choice-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:6px}.hd-choice-grid button{min-width:0;min-height:58px;padding:7px 3px;border-radius:10px;background:linear-gradient(145deg,#29475b,#39435d);border:1px solid #9bb8c355;color:#fff;font-size:19px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:3px}.hd-choice-grid button b{font-size:8px}.hd-furniture-grid button{background:linear-gradient(145deg,#58465b,#384765);border-color:#d2a7bc55}.hd-help{font-size:8px;color:#c4d8e1;line-height:1.5;margin:8px 1px 0}.hd-empty{font-size:9px;color:#c4d8e1;padding:8px 2px}.hd-label{display:block;font-size:9px;font-weight:800;color:#d9e9ed;margin:6px 0 2px}.hd-panel .field{padding:9px;margin:3px 0 7px;font-size:11px}.hd-two-fields{display:grid;grid-template-columns:1fr 1fr;gap:8px}.hd-color{width:100%;height:36px;border:1px solid #ffffff55;border-radius:9px;background:#ffffff18;padding:3px}.hd-action-row{display:flex;gap:6px;flex-wrap:wrap;margin-top:8px}.hd-action{flex:1;min-width:0;padding:9px 6px;border-radius:9px;background:linear-gradient(110deg,#d5ad7c,#a8c7d8);color:#182d3c;font-size:8px;font-weight:900;border:1px solid #ffffff45}.hd-action.danger{background:linear-gradient(110deg,#ff9a9c,#e66c79);color:#431c2a}.hd-status{font-size:8px;color:#c5e7dc;min-height:14px;margin:8px 2px 0}.hd-project-actions .hd-action{flex:1 1 42%}
@media(max-width:370px){.hd-hero{padding:12px}.hd-choice-grid{gap:4px}.hd-choice-grid button{min-height:53px}.hd-panel{padding:9px}.hd-action{font-size:7px;padding:8px 4px}}



/* CREATIVE STUDIO — dedicated page atmosphere */
.screen:has(#studio-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#ffbd8a66,transparent 34%),radial-gradient(circle at 92% 18%,#8c79ff66,transparent 36%),radial-gradient(circle at 50% 100%,#6de5c844,transparent 42%),linear-gradient(145deg,#28264b,#50345f 54%,#285b69)}
.screen:has(#weather-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#ffdf8a66,transparent 34%),radial-gradient(circle at 92% 18%,#65cfff55,transparent 36%),linear-gradient(145deg,#17465e,#277e91 55%,#465c83)}
.screen:has(#breakout-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#ff6eab55,transparent 34%),radial-gradient(circle at 92% 18%,#6e8dff55,transparent 36%),linear-gradient(145deg,#251c49,#492d70 55%,#793b68)}
.screen:has(#pin-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#70e9c955,transparent 34%),radial-gradient(circle at 92% 18%,#7e9fff55,transparent 36%),linear-gradient(145deg,#153d50,#24566b 55%,#3b3e70)}
.studio-hero{padding:15px;border-radius:19px;background:radial-gradient(circle at 90% 0%,#ffb77c55,transparent 45%),linear-gradient(145deg,#292b50,#56345f 58%,#23566a);border:1px solid #ffffff35;box-shadow:0 13px 28px #10152c55}
.studio-kicker{font-size:8px;letter-spacing:2px;color:#ffd59b;font-weight:900}
.studio-hero h2{font-size:22px;color:#fff;margin:8px 0}.studio-hero p{font-size:10px;line-height:1.55;color:#e5dff4;margin:0}
.studio-stats{display:flex;gap:7px;margin-top:13px}.studio-stats span{flex:1;padding:8px 5px;border-radius:10px;background:#ffffff13;border:1px solid #ffffff22;text-align:center;font-size:7px;letter-spacing:1px;color:#f4e9ff}.studio-stats b{display:block;font-size:14px;color:#ffd59b;margin-bottom:3px}
.studio-toolbar{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:5px;margin:11px 0}.studio-tool{padding:10px 2px;border-radius:10px;background:#ffffff18;border:1px solid #ffffff35;color:#fff;font-size:9px;font-weight:800}.studio-tool.active{background:linear-gradient(135deg,#ffb978,#e78ca9);border-color:#ffe2c4;color:#302642}
.studio-board-wrap{padding:8px;border-radius:16px;background:linear-gradient(145deg,#ffffff22,#ffffff0c);border:1px solid #ffffff40;box-shadow:0 10px 25px #11152d55}.studio-board-head{display:flex;align-items:center;justify-content:space-between;gap:8px;padding:2px 3px 8px;color:#fff;font-size:9px;letter-spacing:1px}.studio-board-head span{font-size:8px;color:#f5d8b8;letter-spacing:0;text-align:right}
#studio-canvas{display:block;width:100%;height:auto;aspect-ratio:900/650;border-radius:10px;background:#fff;touch-action:none;cursor:crosshair;box-shadow:inset 0 0 0 1px #1c294022}
.studio-panel{margin-top:10px;padding:12px;border-radius:15px;background:linear-gradient(145deg,#ffffff1d,#ffffff0b);border:1px solid #ffffff30}.studio-panel-title{font-size:11px;font-weight:900;color:#fff;margin-bottom:10px}.studio-controls-grid{display:grid;grid-template-columns:1fr 1fr;gap:10px}.studio-control{display:grid;gap:7px;font-size:9px;color:#f1eaff}.studio-control b{color:#ffd59b}.studio-control input[type=color]{width:100%;height:36px;padding:2px;border:1px solid #ffffff55;border-radius:9px;background:#ffffff20}.studio-control input[type=range]{width:100%;accent-color:#ffbc83}
.studio-swatches{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}.studio-swatches button{width:27px;height:27px;border-radius:50%;background:var(--swatch);border:2px solid #ffffffb0;box-shadow:0 2px 7px #0004}.studio-backgrounds{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:6px}.studio-bg-choice{padding:9px 3px;border-radius:9px;background:#ffffff18;border:1px solid #ffffff35;color:#fff;font-size:9px}.studio-bg-choice.active{background:#ffcf9b;color:#392d43;border-color:#fff0d8;font-weight:900}
.studio-actions{display:grid;grid-template-columns:1fr 1fr 1.35fr;gap:7px;margin-top:11px}.studio-actions button{padding:11px 5px;border-radius:10px;background:#ffffff20;border:1px solid #ffffff45;color:#fff;font-size:9px;font-weight:900}.studio-actions .studio-save{background:linear-gradient(110deg,#ffd18f,#f19bb1);color:#382a43;border-color:#ffe6c7}.studio-footnote{font-size:8px;line-height:1.5;color:#e4d9f2;margin:9px 2px 0}
@media(max-width:360px){.studio-tool{font-size:8px;padding:9px 1px}.studio-actions{grid-template-columns:1fr 1fr}.studio-actions .studio-save{grid-column:1/-1}}


/* DISTINCT PAGE THEMES: every app and game receives its own visual identity. */
.screen:has(#weather-page:not(.hidden)){background:radial-gradient(circle at 80% 8%,#ffe8a7 0 5%,transparent 34%),linear-gradient(145deg,#183e72,#267f9b 52%,#78b8b1)}
.screen:has(#house-page:not(.hidden)){background:radial-gradient(circle at 10% 10%,#f2c88c55,transparent 34%),linear-gradient(145deg,#46352d,#89634a 55%,#b58a61)}
.screen:has(#shopping-page:not(.hidden)){background:radial-gradient(circle at 90% 10%,#ff91ae55,transparent 35%),linear-gradient(145deg,#541e48,#a63869 55%,#e47b72)}
.screen:has(#breakout-page:not(.hidden)){background:radial-gradient(circle at 50% 0%,#55eaff55,transparent 40%),linear-gradient(145deg,#07101e,#171b3b 55%,#39215c)}
.screen:has(#calculator-page:not(.hidden)){background:radial-gradient(circle at 85% 10%,#ffd16a55,transparent 35%),linear-gradient(145deg,#563326,#a65c35 55%,#d18b49)}
.screen:has(#password-page:not(.hidden)){background:radial-gradient(circle at 85% 12%,#7df4ff55,transparent 36%),linear-gradient(145deg,#12334c,#176b83 55%,#3b9c9a)}
.screen:has(#notes-page:not(.hidden)){background:radial-gradient(circle at 10% 5%,#ffe3a455,transparent 34%),linear-gradient(145deg,#51412b,#8a7040 55%,#b59a62)}
.screen:has(#guess-page:not(.hidden)){background:radial-gradient(circle at 80% 8%,#ffda7755,transparent 36%),linear-gradient(145deg,#682d36,#a44b3e 55%,#ce8752)}
.screen:has(#typing-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#c7a5ff55,transparent 34%),linear-gradient(145deg,#29204f,#584080 55%,#95609a)}
.screen:has(#flappy-page:not(.hidden)){background:radial-gradient(circle at 80% 8%,#fff3a055,transparent 34%),linear-gradient(145deg,#16617d,#32a0a4 55%,#a1c987)}
.screen:has(#snake-page:not(.hidden)){background:radial-gradient(circle at 12% 10%,#a5ff7655,transparent 35%),linear-gradient(145deg,#102d23,#176343 55%,#3c8a55)}
.screen:has(#car-page:not(.hidden)){background:radial-gradient(circle at 90% 8%,#ffcf6c55,transparent 35%),linear-gradient(145deg,#3b2930,#85433d 55%,#c47b43)}
.screen:has(#settings-page:not(.hidden)){background:radial-gradient(circle at 10% 8%,#ffadd355,transparent 35%),linear-gradient(145deg,#512c54,#914d78 55%,#bd7992)}
.screen:has(#about-page:not(.hidden)){background:radial-gradient(circle at 85% 10%,#ffe69c55,transparent 35%),linear-gradient(145deg,#534027,#9b7440 55%,#c5a66b)}
.screen:has(#school-page:not(.hidden)){background:radial-gradient(circle at 12% 8%,#9de7ff55,transparent 35%),linear-gradient(145deg,#183c5e,#287d89 55%,#72a8a0)}
.screen:has(#school-history-page:not(.hidden)){background:radial-gradient(circle at 90% 8%,#ffcd8355,transparent 35%),linear-gradient(145deg,#4c3028,#936143 55%,#c28a58)}
.screen:has(#school-mission-page:not(.hidden)){background:radial-gradient(circle at 8% 8%,#c3a0ff55,transparent 35%),linear-gradient(145deg,#302850,#634b88 55%,#9a7099)}
.screen:has(#solar-page:not(.hidden)){background:radial-gradient(circle at 50% 5%,#8f9eff55,transparent 38%),linear-gradient(145deg,#030914,#0b2342 55%,#202c55)}
.screen:has(#studio-page:not(.hidden)){background:radial-gradient(circle at 85% 5%,#ffb0d655,transparent 35%),linear-gradient(145deg,#4c2057,#913d75 52%,#d06b75)}
.screen:has(#quran-page:not(.hidden)){background:radial-gradient(circle at 85% 8%,#e5d08c55,transparent 34%),linear-gradient(145deg,#123b37,#176a5c 55%,#9b8751)}
.screen:has(#pin-page:not(.hidden)){background:radial-gradient(circle at 50% 5%,#9bdfff55,transparent 35%),linear-gradient(145deg,#102c52,#24558b 55%,#477caa)}
.screen:has(#app-login-page:not(.hidden)){background:radial-gradient(circle at 90% 8%,#ffa2b655,transparent 35%),linear-gradient(145deg,#48223d,#813e5e 55%,#b46a73)}
#studio-page .studio-hero{background:linear-gradient(135deg,#59275f,#a33f76 55%,#d16b70)!important}
#studio-page .studio-panel{background:linear-gradient(135deg,#39244e,#68406e)!important;border-color:#ffb6dc!important}
#studio-page .studio-board-wrap{background:linear-gradient(135deg,#7b3c70,#b85a7b)!important}
#studio-page .studio-extra-tools{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:7px}
#studio-page .studio-extra-tools button{padding:11px 7px;border-radius:11px;background:linear-gradient(135deg,#f5c5e5,#e99cbe);color:#54294a;font-size:11px}
#studio-canvas{touch-action:none;cursor:crosshair}
#app-loading-overlay{position:absolute;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;background:linear-gradient(145deg,#101d3d,#39245b 55%,#75436d);color:#fff;transition:opacity .18s ease}
#app-loading-overlay b{font-size:14px;letter-spacing:3px}
.app-loader-orbit{width:48px;height:48px;position:relative;border:3px solid #ffffff30;border-top-color:#8effd6;border-right-color:#c59cff;border-radius:50%;animation:appSpin .72s linear infinite}
.app-loader-orbit i{position:absolute;width:7px;height:7px;border-radius:50%;background:#ffe18a;top:-4px;left:18px;box-shadow:0 0 10px #ffe18a}
.app-loader-orbit i:nth-child(2){top:17px;left:40px;background:#8effed}
.app-loader-orbit i:nth-child(3){top:38px;left:7px;background:#d3a0ff}
@keyframes appSpin{to{transform:rotate(360deg)}}


/* DISTINCT PAGE ENVIRONMENTS */
.screen:has(#login-page:not(.hidden)){background:radial-gradient(ellipse at 18% 8%,#f6c3ff66,transparent 35%),linear-gradient(145deg,#241b43,#51305c 55%,#8c456b)}
.screen:has(#app-login-page:not(.hidden)){background:radial-gradient(ellipse at 85% 12%,#ffb28b66,transparent 35%),linear-gradient(145deg,#43243b,#873f58 55%,#b96b64)}
.screen:has(#home-page:not(.hidden)){background:radial-gradient(ellipse at 8% 8%,#ffc86a66,transparent 34%),linear-gradient(145deg,#173d55,#315c68 55%,#68506f)}
.screen:has(#weather-page:not(.hidden)){background:radial-gradient(ellipse at 80% 10%,#b9f6ff77,transparent 36%),linear-gradient(145deg,#073c58,#137e91 55%,#65b8a5)}
.screen:has(#house-page:not(.hidden)){background:radial-gradient(ellipse at 10% 12%,#ffe0a566,transparent 34%),linear-gradient(145deg,#3a2b26,#78523c 55%,#bd8c5e)}
.screen:has(#shopping-page:not(.hidden)){background:radial-gradient(ellipse at 88% 8%,#ff9dc977,transparent 34%),linear-gradient(145deg,#351d49,#78345f 55%,#b65b72)}
.screen:has(#breakout-page:not(.hidden)){background:radial-gradient(ellipse at 50% 0%,#69f3ff66,transparent 38%),linear-gradient(145deg,#080e27,#25245b 55%,#66366e)}
.screen:has(#calculator-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#ffe38a77,transparent 34%),linear-gradient(145deg,#49301f,#986039 55%,#d39a54)}
.screen:has(#password-page:not(.hidden)){background:radial-gradient(ellipse at 8% 8%,#9df7ff66,transparent 34%),linear-gradient(145deg,#092e49,#176d83 55%,#458f9c)}
.screen:has(#notes-page:not(.hidden)){background:radial-gradient(ellipse at 90% 8%,#ffe7a577,transparent 34%),linear-gradient(145deg,#3e3525,#80683b 55%,#b59a61)}
.screen:has(#games-page:not(.hidden)){background:radial-gradient(ellipse at 10% 5%,#8effd566,transparent 35%),linear-gradient(145deg,#102f43,#285d69 55%,#477b75)}
.screen:has(#guess-page:not(.hidden)){background:radial-gradient(ellipse at 80% 10%,#ffd47a77,transparent 34%),linear-gradient(145deg,#56283a,#9c493e 55%,#d18450)}
.screen:has(#typing-page:not(.hidden)){background:radial-gradient(ellipse at 10% 8%,#d7b4ff77,transparent 35%),linear-gradient(145deg,#292044,#58417e 55%,#9b6596)}
.screen:has(#flappy-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#fff5a577,transparent 34%),linear-gradient(145deg,#12516d,#2699a1 55%,#9cc985)}
.screen:has(#snake-page:not(.hidden)){background:radial-gradient(ellipse at 12% 8%,#c2ff8a66,transparent 34%),linear-gradient(145deg,#102c25,#17664a 55%,#4b9b60)}
.screen:has(#car-page:not(.hidden)){background:radial-gradient(ellipse at 88% 8%,#ffc07877,transparent 34%),linear-gradient(145deg,#352333,#75404b 55%,#b96c43)}
.screen:has(#settings-page:not(.hidden)){background:radial-gradient(ellipse at 8% 8%,#ffb8dc77,transparent 34%),linear-gradient(145deg,#48254e,#854c7d 55%,#b982a0)}
.screen:has(#about-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#fff0a577,transparent 34%),linear-gradient(145deg,#45351f,#8c6838 55%,#c4a36a)}
.screen:has(#school-page:not(.hidden)){background:radial-gradient(ellipse at 10% 8%,#a8edff77,transparent 34%),linear-gradient(145deg,#153955,#287c91 55%,#6da99b)}
.screen:has(#school-history-page:not(.hidden)){background:radial-gradient(ellipse at 90% 8%,#ffd09a77,transparent 34%),linear-gradient(145deg,#452b26,#965d3e 55%,#c58d58)}
.screen:has(#school-mission-page:not(.hidden)){background:radial-gradient(ellipse at 10% 8%,#d4b4ff77,transparent 34%),linear-gradient(145deg,#302548,#654b85 55%,#a17da2)}
.screen:has(#solar-page:not(.hidden)){background:radial-gradient(ellipse at 50% 5%,#a1b5ff66,transparent 38%),linear-gradient(145deg,#020711,#102747 55%,#283b69)}
.screen:has(#studio-page:not(.hidden)){background:radial-gradient(ellipse at 85% 5%,#ffb7d977,transparent 35%),linear-gradient(145deg,#48234d,#963d75 55%,#d47b75)}
.screen:has(#quran-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#f2dfa577,transparent 34%),linear-gradient(145deg,#103b36,#1c6b5c 55%,#9c8953)}
.screen:has(#pin-page:not(.hidden)){background:radial-gradient(ellipse at 50% 5%,#9be6ff77,transparent 35%),linear-gradient(145deg,#102a4d,#245b8a 55%,#5794b0)}

.game3d-layer{border-radius:inherit;overflow:hidden;filter:saturate(1.08) contrast(1.02)}
.mini-3d-game{display:block;width:100%;height:126px;margin:0 0 10px;border-radius:14px;background:linear-gradient(135deg,#111d37,#4c3b73);}

/* LOGIN POLISH: clear vertical rhythm between the clock, welcome copy and actions. */
#login-page.login-wrap{min-height:690px;justify-content:flex-start;padding:38px 7px 24px;gap:0}
#login-page .clock-panel{transform:none!important;margin:0 auto 27px;padding:17px 14px;gap:18px;min-height:150px}
#login-page .login-title{font-family:Georgia,'Times New Roman',serif;font-size:39px;font-weight:1000;letter-spacing:1.8px;text-shadow:0 5px 20px #10152d66;filter:drop-shadow(0 2px 1px #ffffff25)}
#login-page h2{font-size:16px;font-weight:900;letter-spacing:.25px;margin:8px 0 27px!important;text-shadow:0 2px 9px #07162988}
#login-page .login-actions{transform:none!important;gap:12px;max-width:320px}
#login-page .login-actions button{min-height:52px;font-size:13px;letter-spacing:1.1px;border-radius:17px}
#login-page .time-info{padding-left:2px}
#login-page .digital-time{font-size:26px;font-weight:1000;letter-spacing:1.2px;text-shadow:0 2px 8px #18334c44}
#login-page .digital-date{font-size:11px;font-weight:800;line-height:1.55;letter-spacing:.25px}
@media(max-width:360px){#login-page.login-wrap{padding-top:26px}#login-page .clock-panel{gap:11px;padding:13px 8px;margin-bottom:22px}#login-page .clock-face{width:92px;height:92px}#login-page .digital-time{font-size:20px}#login-page .login-title{font-size:34px}}
/* Each screen gets its own composition, not merely a hue variation. */
.screen:has(#app-login-page:not(.hidden)){background:radial-gradient(circle at 18% 12%,#fff1a855,transparent 24%),radial-gradient(circle at 88% 80%,#ed9bff55,transparent 35%),linear-gradient(125deg,#171d3d 0%,#53365e 48%,#a34f68 100%)}
.screen:has(#home-page:not(.hidden)){background:radial-gradient(ellipse at 0% 0%,#5af1d755,transparent 30%),radial-gradient(ellipse at 100% 100%,#f3b15a55,transparent 35%),linear-gradient(145deg,#123b4c,#1b5860 52%,#36536d)}
.screen:has(#weather-page:not(.hidden)){background:radial-gradient(circle at 80% 10%,#fff2a877,transparent 28%),radial-gradient(circle at 12% 85%,#5fd6ff55,transparent 34%),linear-gradient(150deg,#174c78,#287fa1 52%,#72a9b1)}
.screen:has(#house-page:not(.hidden)){background:repeating-linear-gradient(135deg,#ffffff08 0 2px,transparent 2px 18px),radial-gradient(circle at 90% 8%,#f4c17b66,transparent 30%),linear-gradient(145deg,#3b2c28,#79513d 48%,#b58a60)}
.screen:has(#shopping-page:not(.hidden)){background:radial-gradient(circle at 10% 10%,#ffb1ca77,transparent 30%),radial-gradient(circle at 90% 90%,#9f9bff66,transparent 34%),linear-gradient(135deg,#54244f,#943b71 52%,#4b397e)}
.screen:has(#breakout-page:not(.hidden)){background:radial-gradient(circle at 50% 0%,#45eaff55,transparent 30%),radial-gradient(circle at 50% 100%,#bc54ff55,transparent 36%),linear-gradient(180deg,#050d20,#101b39 55%,#24133c)}
.screen:has(#calculator-page:not(.hidden)){background:radial-gradient(circle at 90% 5%,#ffe58a77,transparent 28%),linear-gradient(150deg,#44301f,#8a542b 52%,#bd7840)}
.screen:has(#password-page:not(.hidden)){background:radial-gradient(circle at 8% 12%,#67f3ff66,transparent 30%),linear-gradient(145deg,#102c4c,#155d78 50%,#267e88)}
.screen:has(#notes-page:not(.hidden)){background:repeating-linear-gradient(0deg,#fff1 0 1px,transparent 1px 28px),linear-gradient(145deg,#51402a,#87613a 55%,#b78a4c)}
.screen:has(#games-page:not(.hidden)){background:radial-gradient(circle at 12% 10%,#a3ffbd55,transparent 30%),radial-gradient(circle at 90% 90%,#ff8bc955,transparent 32%),linear-gradient(135deg,#192c55,#3c3974 52%,#74446c)}
.screen:has(#guess-page:not(.hidden)){background:radial-gradient(circle at 82% 12%,#fff18a77,transparent 25%),linear-gradient(145deg,#4a2633,#88442e 48%,#bd7544)}
.screen:has(#typing-page:not(.hidden)){background:repeating-linear-gradient(115deg,#ffffff09 0 1px,transparent 1px 15px),linear-gradient(145deg,#222244,#4e3878 52%,#875c91)}
.screen:has(#flappy-page:not(.hidden)){background:radial-gradient(circle at 15% 10%,#fff4a877,transparent 30%),linear-gradient(180deg,#155777,#2697a2 55%,#8bbd83)}
.screen:has(#snake-page:not(.hidden)){background:radial-gradient(circle at 85% 12%,#c8ff8a66,transparent 28%),linear-gradient(145deg,#0b3027,#176346 55%,#397b4e)}
.screen:has(#car-page:not(.hidden)){background:radial-gradient(circle at 12% 12%,#ffcf7a66,transparent 28%),radial-gradient(circle at 90% 85%,#ff7a8a55,transparent 34%),linear-gradient(145deg,#262d3e,#5b3944 52%,#9a573f)}
.screen:has(#settings-page:not(.hidden)){background:radial-gradient(circle at 80% 10%,#ffb9e577,transparent 28%),linear-gradient(145deg,#362344,#71436e 52%,#a45b86)}
.screen:has(#about-page:not(.hidden)){background:radial-gradient(circle at 50% 0%,#fff0a877,transparent 30%),linear-gradient(145deg,#3c3524,#76613a 50%,#b39457)}
.screen:has(#school-page:not(.hidden)){background:radial-gradient(circle at 15% 12%,#8feaff77,transparent 30%),linear-gradient(145deg,#123b58,#26768b 52%,#72a7a0)}
.screen:has(#school-history-page:not(.hidden)){background:repeating-linear-gradient(90deg,#ffffff08 0 2px,transparent 2px 22px),linear-gradient(145deg,#42271f,#895239 52%,#c18b53)}
.screen:has(#school-mission-page:not(.hidden)){background:radial-gradient(circle at 88% 12%,#e4b5ff77,transparent 30%),linear-gradient(145deg,#292344,#59417d 52%,#9875a0)}
.screen:has(#solar-page:not(.hidden)){background:radial-gradient(ellipse at 50% 35%,#234d85 0%,#101a3d 38%,#030712 78%);}
.screen:has(#studio-page:not(.hidden)){background:radial-gradient(circle at 12% 10%,#ffb5db77,transparent 28%),radial-gradient(circle at 90% 90%,#9df7dd55,transparent 34%),linear-gradient(135deg,#47224f,#9b3f78 52%,#d16c70)}
.screen:has(#quran-page:not(.hidden)){background:radial-gradient(circle at 80% 8%,#f4d58b77,transparent 28%),linear-gradient(145deg,#0e3938,#176458 52%,#7c7948)}
.screen:has(#pin-page:not(.hidden)){background:radial-gradient(circle at 50% 0%,#a8e8ff77,transparent 28%),linear-gradient(145deg,#12294b,#275c8d 52%,#477d9d)}
/* Flappy stays a classic 2D canvas game; no decorative 3D layer over it. */
#flappy-canvas{opacity:1!important;position:relative;z-index:1;box-shadow:0 10px 25px #082b4266,inset 0 0 0 1px #ffffff66}
#flappy-page .card{background:linear-gradient(145deg,#ffffff24,#ffffff0d);border-color:#b9f4ff88}
/* Racing canvas has a complete roadside scene and premium vehicle artwork. */
#car-canvas{opacity:1!important;position:relative;z-index:1;width:100%;height:auto;aspect-ratio:2/3;max-height:none;background:#1c4b39;box-shadow:0 12px 28px #071a2b88,inset 0 0 0 1px #ffffff66}


/* FINAL REFINEMENT: unmistakably different screen environments, not one shared gradient. */
.screen:has(#login-page:not(.hidden)){background:radial-gradient(circle at 82% 13%,rgba(255,211,125,.28),transparent 22%),radial-gradient(circle at 12% 80%,rgba(83,225,219,.22),transparent 29%),repeating-linear-gradient(135deg,rgba(255,255,255,.025) 0 1px,transparent 1px 13px),linear-gradient(150deg,#111b3b 0%,#273d68 46%,#68446d 100%) !important;}
.screen:has(#app-login-page:not(.hidden)){background:radial-gradient(ellipse at 50% 0%,rgba(103,225,255,.3),transparent 36%),radial-gradient(circle at 100% 100%,rgba(135,111,255,.25),transparent 34%),repeating-linear-gradient(90deg,rgba(255,255,255,.025) 0 1px,transparent 1px 18px),linear-gradient(145deg,#082b3a,#10536a 48%,#1c315e) !important;}
.screen:has(#home-page:not(.hidden)){background:radial-gradient(circle at 12% 12%,rgba(255,191,105,.35),transparent 25%),radial-gradient(circle at 92% 82%,rgba(255,111,139,.22),transparent 31%),repeating-linear-gradient(45deg,rgba(255,255,255,.025) 0 2px,transparent 2px 16px),linear-gradient(145deg,#39213c,#75404b 52%,#b06a48) !important;}
.screen:has(#weather-page:not(.hidden)){background:radial-gradient(circle at 80% 18%,#fff0a966,transparent 25%),linear-gradient(155deg,#123e66,#267e9c 52%,#a0b9a1) !important;}
.screen:has(#house-page:not(.hidden)){background:repeating-linear-gradient(0deg,#ffffff09 0 1px,transparent 1px 22px),linear-gradient(145deg,#342b27,#74513d 48%,#b28b62) !important;}
.screen:has(#shopping-page:not(.hidden)){background:radial-gradient(circle at 10% 12%,#ff9cb966,transparent 28%),radial-gradient(circle at 90% 85%,#ffc56b55,transparent 28%),linear-gradient(145deg,#4a2146,#913f68 52%,#bd755e) !important;}
.screen:has(#breakout-page:not(.hidden)){background:radial-gradient(circle at 50% 0%,#3267a777,transparent 38%),repeating-linear-gradient(135deg,#ffffff08 0 1px,transparent 1px 12px),linear-gradient(155deg,#050b1b,#171b3b 54%,#311b45) !important;}
.screen:has(#calculator-page:not(.hidden)){background:radial-gradient(circle at 88% 12%,#ffd36c66,transparent 25%),linear-gradient(145deg,#38231d,#84502d 52%,#b27b42) !important;}
.screen:has(#password-page:not(.hidden)){background:repeating-linear-gradient(90deg,#b9f4ff0b 0 1px,transparent 1px 20px),linear-gradient(145deg,#082b48,#075b70 52%,#347f87) !important;}
.screen:has(#notes-page:not(.hidden)){background:repeating-linear-gradient(0deg,#ffe5a018 0 1px,transparent 1px 23px),linear-gradient(145deg,#44311e,#80603b 50%,#b38b53) !important;}
.screen:has(#games-page:not(.hidden)){background:radial-gradient(circle at 15% 12%,#ff6a9a66,transparent 27%),radial-gradient(circle at 90% 80%,#5c9dff55,transparent 32%),linear-gradient(145deg,#211d50,#49316f 54%,#813e75) !important;}
.screen:has(#guess-page:not(.hidden)){background:radial-gradient(circle at 50% 0%,#ffdf7b66,transparent 28%),repeating-linear-gradient(45deg,#ffffff08 0 2px,transparent 2px 15px),linear-gradient(145deg,#4b2b23,#9b5632 55%,#69406b) !important;}
.screen:has(#typing-page:not(.hidden)){background:repeating-linear-gradient(0deg,#ffffff0b 0 1px,transparent 1px 19px),linear-gradient(145deg,#252344,#4b477d 52%,#7b567b) !important;}
.screen:has(#flappy-page:not(.hidden)){background:radial-gradient(circle at 80% 12%,#ffe69a66,transparent 25%),linear-gradient(180deg,#347fa7 0%,#4fa8b0 48%,#497b62 100%) !important;}
.screen:has(#snake-page:not(.hidden)){background:radial-gradient(circle at 12% 12%,#b8f07855,transparent 26%),repeating-linear-gradient(135deg,#d9ffcf09 0 1px,transparent 1px 14px),linear-gradient(145deg,#102f25,#1b6544 52%,#315b4a) !important;}
.screen:has(#car-page:not(.hidden)){background:radial-gradient(ellipse at 50% 0%,#f3bb7755,transparent 36%),repeating-linear-gradient(90deg,#ffffff08 0 1px,transparent 1px 20px),linear-gradient(145deg,#242c35,#46505a 52%,#73564a) !important;}
.screen:has(#settings-page:not(.hidden)){background:radial-gradient(circle at 88% 10%,#ffb5db66,transparent 26%),linear-gradient(145deg,#38233f,#75405f 52%,#a15b76) !important;}
.screen:has(#about-page:not(.hidden)){background:radial-gradient(circle at 12% 10%,#ffe4a366,transparent 26%),repeating-linear-gradient(135deg,#ffffff08 0 1px,transparent 1px 17px),linear-gradient(145deg,#3b3426,#78603a 52%,#a77b50) !important;}
.screen:has(#school-page:not(.hidden)){background:radial-gradient(circle at 12% 12%,#e4d39a66,transparent 28%),linear-gradient(145deg,#173c54,#3e7881 52%,#8a7655) !important;}
.screen:has(#school-history-page:not(.hidden)){background:repeating-linear-gradient(0deg,#e7d2a015 0 1px,transparent 1px 21px),radial-gradient(circle at 88% 10%,#d5b47766,transparent 27%),linear-gradient(145deg,#493725,#82613c 54%,#b28a55) !important;}
.screen:has(#school-mission-page:not(.hidden)){background:radial-gradient(circle at 12% 10%,#b8a2ff66,transparent 28%),repeating-linear-gradient(135deg,#ffffff0a 0 1px,transparent 1px 16px),linear-gradient(145deg,#292447,#574477 54%,#8d668d) !important;}
.screen:has(#solar-page:not(.hidden)){background:radial-gradient(ellipse at 50% 30%,#254b83 0%,#111b3e 38%,#02050d 82%) !important;}
.screen:has(#studio-page:not(.hidden)){background:radial-gradient(circle at 10% 12%,#ffb0dc77,transparent 27%),radial-gradient(circle at 92% 90%,#9bffe477,transparent 29%),repeating-linear-gradient(135deg,#ffffff0b 0 2px,transparent 2px 17px),linear-gradient(145deg,#51214f,#9a3f76 54%,#ce6e68) !important;}
.screen:has(#quran-page:not(.hidden)){background:radial-gradient(circle at 85% 12%,#e9ca7c66,transparent 25%),repeating-linear-gradient(45deg,#ffffff08 0 1px,transparent 1px 18px),linear-gradient(145deg,#0c3435,#176354 52%,#6d7044) !important;}
.screen:has(#pin-page:not(.hidden)){background:radial-gradient(circle at 50% 0%,#a7e8ff77,transparent 30%),linear-gradient(145deg,#102443,#285d8c 54%,#568b9c) !important;}
.screen:has(#login-page:not(.hidden)) .login-actions button{border-radius:19px;letter-spacing:1.1px;}
.screen:has(#app-login-page:not(.hidden)) .primary{background:linear-gradient(100deg,#70e6ef,#8cbcff,#c5a5ff);color:#102b45;}
.screen:has(#home-page:not(.hidden)) .tile,.screen:has(#home-page:not(.hidden)) .home-shortcut{background:linear-gradient(145deg,#8c4c53,#58365e 58%,#344b6b)!important;border-color:#ffc28b;}
.screen:has(#calculator-page:not(.hidden)) .calc-key{background:linear-gradient(145deg,#fff5df,#e9c99a);border:1px solid #fff0d0;}
.screen:has(#calculator-page:not(.hidden)) .calc-key.op{background:linear-gradient(145deg,#ffc96e,#e98d46);}
.screen:has(#password-page:not(.hidden)) button.primary{background:linear-gradient(100deg,#70e8ed,#58b9d5);color:#083448;}
.screen:has(#notes-page:not(.hidden)) button.primary{background:linear-gradient(100deg,#f5d48b,#c99557);color:#3d2b1c;}
.screen:has(#games-page:not(.hidden)) .tile{background:linear-gradient(145deg,#7652ad,#3c397d)!important;border-color:#c8b0ff;}
.screen:has(#flappy-page:not(.hidden)) button.primary{background:linear-gradient(100deg,#ffe18a,#ffad64);color:#55331d;}
.screen:has(#snake-page:not(.hidden)) button.primary{background:linear-gradient(100deg,#b8ed75,#55c78b);color:#163e2b;}
.screen:has(#car-page:not(.hidden)) .car-controls button{background:linear-gradient(145deg,#ffe0a0,#d48a56);color:#462b1d;}
.screen:has(#settings-page:not(.hidden)) button.primary{background:linear-gradient(100deg,#ffb4d6,#c19cff);color:#47264c;}
.screen:has(#about-page:not(.hidden)) button.primary{background:linear-gradient(100deg,#ffe2a0,#e3a86c);color:#49331d;}
.screen:has(#studio-page:not(.hidden)) button{border-radius:12px;}
#app-login-page .login-wrap{min-height:0!important;justify-content:flex-start;padding-top:18px;padding-bottom:18px;gap:0;}
#app-login-page .login-wrap>h2{margin:3px 0 9px!important;}
#app-login-page .card{padding:13px!important;margin:0 auto!important;}
#app-login-page .card label{display:block;margin:5px 0 2px;font-size:12px;font-weight:800;color:#e7f8ff;}
#app-login-page .field{margin:2px 0 7px;padding:11px 12px;}
#app-login-page .primary{margin-top:4px;padding:12px;}
#app-login-page .secondary{margin-top:8px!important;padding:11px;}
#login-page .login-wrap{min-height:590px;}
#login-page .clock-panel{margin-bottom:11px;}
#login-page .login-title{margin-top:0;}
#login-page .login-sub{margin-bottom:10px;}
#car-canvas{display:block!important;position:relative!important;inset:auto!important;float:none!important;clear:both!important;width:min(100%,310px)!important;min-width:0!important;height:auto!important;aspect-ratio:340/510!important;max-height:none!important;object-fit:fill!important;object-position:center!important;margin:0 auto 7px!important;transform:none!important;animation:none!important;flex:none!important;}
#car-page .card{overflow:hidden;}#car-page{overflow-x:hidden;}#car-page .car-score{width:100%;}
#flappy-canvas{display:block;width:100%;height:auto;aspect-ratio:360/460;max-height:none;object-fit:contain;}
#snake-canvas{display:block;width:min(100%,288px);height:auto;aspect-ratio:1/1;object-fit:contain;}


/* UNIQUE MULTI-COLOUR BACKDROPS — each page blends three clearly different hues. */
.screen:has(#login-page:not(.hidden)){background:radial-gradient(ellipse at 12% 12%,#f7c86b88,transparent 34%),radial-gradient(ellipse at 90% 88%,#58d9ce66,transparent 38%),linear-gradient(135deg,#19264f 0%,#57406f 52%,#a45b65 100%)!important;}
.screen:has(#app-login-page:not(.hidden)){background:radial-gradient(ellipse at 90% 8%,#68d9ff88,transparent 34%),radial-gradient(ellipse at 8% 92%,#ff9eaa66,transparent 36%),linear-gradient(140deg,#12334f 0%,#235c78 50%,#554078 100%)!important;}
.screen:has(#home-page:not(.hidden)){background:radial-gradient(ellipse at 10% 8%,#ffcb6f99,transparent 34%),radial-gradient(ellipse at 92% 88%,#74e4c577,transparent 36%),linear-gradient(140deg,#49304f 0%,#8a465e 50%,#315b78 100%)!important;}
.screen:has(#weather-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#fff08c99,transparent 32%),radial-gradient(ellipse at 8% 92%,#6fe5d777,transparent 38%),linear-gradient(145deg,#174b79 0%,#278da7 52%,#647eaa 100%)!important;}
.screen:has(#house-page:not(.hidden)){background:radial-gradient(ellipse at 8% 10%,#e5b27b88,transparent 35%),radial-gradient(ellipse at 92% 90%,#8ec5ba77,transparent 38%),linear-gradient(145deg,#49342d 0%,#88634b 52%,#4d6470 100%)!important;}
.screen:has(#shopping-page:not(.hidden)){background:radial-gradient(ellipse at 90% 8%,#ff9dbb99,transparent 34%),radial-gradient(ellipse at 8% 92%,#ffc36b77,transparent 36%),linear-gradient(145deg,#55264f 0%,#a44372 52%,#684b86 100%)!important;}
.screen:has(#breakout-page:not(.hidden)){background:radial-gradient(ellipse at 50% 4%,#42eaff88,transparent 36%),radial-gradient(ellipse at 90% 90%,#ff5caa66,transparent 38%),linear-gradient(145deg,#071329 0%,#20285a 52%,#492653 100%)!important;}
.screen:has(#calculator-page:not(.hidden)){background:radial-gradient(ellipse at 90% 8%,#ffd36d99,transparent 33%),radial-gradient(ellipse at 8% 90%,#ff8c6b77,transparent 36%),linear-gradient(145deg,#503026 0%,#a45a38 52%,#674b75 100%)!important;}
.screen:has(#password-page:not(.hidden)){background:radial-gradient(ellipse at 10% 10%,#72eaff88,transparent 34%),radial-gradient(ellipse at 90% 90%,#8bf1bd77,transparent 38%),linear-gradient(145deg,#12344e 0%,#176d82 52%,#405c91 100%)!important;}
.screen:has(#notes-page:not(.hidden)){background:radial-gradient(ellipse at 90% 8%,#ffe19a99,transparent 34%),radial-gradient(ellipse at 8% 92%,#c5a2ff66,transparent 36%),linear-gradient(145deg,#493624 0%,#8b6840 52%,#596080 100%)!important;}
.screen:has(#games-page:not(.hidden)){background:radial-gradient(ellipse at 10% 10%,#ff79a799,transparent 34%),radial-gradient(ellipse at 90% 90%,#68caff77,transparent 38%),linear-gradient(145deg,#25204d 0%,#604078 52%,#963f72 100%)!important;}
.screen:has(#guess-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#ffe07899,transparent 34%),radial-gradient(ellipse at 8% 92%,#72e7d477,transparent 38%),linear-gradient(145deg,#56302e 0%,#a7533d 52%,#465d78 100%)!important;}
.screen:has(#typing-page:not(.hidden)){background:radial-gradient(ellipse at 8% 8%,#c9a0ff99,transparent 34%),radial-gradient(ellipse at 92% 92%,#ff9ab477,transparent 38%),linear-gradient(145deg,#28264e 0%,#55427d 52%,#7c496f 100%)!important;}
.screen:has(#flappy-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#ffe88b99,transparent 34%),radial-gradient(ellipse at 8% 90%,#75e1bd77,transparent 38%),linear-gradient(145deg,#1d5b83 0%,#369ca8 52%,#678b61 100%)!important;}
.screen:has(#snake-page:not(.hidden)){background:radial-gradient(ellipse at 8% 8%,#c4f27a99,transparent 34%),radial-gradient(ellipse at 92% 90%,#6edcff77,transparent 38%),linear-gradient(145deg,#123a2b 0%,#20714b 52%,#345d76 100%)!important;}
.screen:has(#car-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#ffd17b99,transparent 34%),radial-gradient(ellipse at 8% 90%,#8fe1cf77,transparent 38%),linear-gradient(145deg,#293744 0%,#745047 52%,#375d70 100%)!important;}
.screen:has(#settings-page:not(.hidden)){background:radial-gradient(ellipse at 8% 8%,#ff9ecb99,transparent 34%),radial-gradient(ellipse at 92% 90%,#9ac4ff77,transparent 38%),linear-gradient(145deg,#45284e 0%,#8b4775 52%,#435b83 100%)!important;}
.screen:has(#about-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#ffe49a99,transparent 34%),radial-gradient(ellipse at 8% 90%,#8be0c677,transparent 38%),linear-gradient(145deg,#4a3929 0%,#907044 52%,#3d6970 100%)!important;}
.screen:has(#school-page:not(.hidden)){background:radial-gradient(ellipse at 8% 8%,#a6e7ff99,transparent 34%),radial-gradient(ellipse at 92% 90%,#f4cf7b77,transparent 38%),linear-gradient(145deg,#193e61 0%,#347e8a 52%,#74634f 100%)!important;}
.screen:has(#school-history-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#ffd08b99,transparent 34%),radial-gradient(ellipse at 8% 90%,#93c5ff77,transparent 38%),linear-gradient(145deg,#503329 0%,#98613f 52%,#425a79 100%)!important;}
.screen:has(#school-mission-page:not(.hidden)){background:radial-gradient(ellipse at 8% 8%,#c8a8ff99,transparent 34%),radial-gradient(ellipse at 92% 90%,#7de2d277,transparent 38%),linear-gradient(145deg,#30264f 0%,#624981 52%,#28716e 100%)!important;}
.screen:has(#solar-page:not(.hidden)){background:radial-gradient(ellipse at 50% 25%,#ffbd6e88,transparent 35%),radial-gradient(ellipse at 90% 90%,#657fff77,transparent 40%),linear-gradient(145deg,#030916 0%,#10284b 52%,#34244f 100%)!important;}
.screen:has(#studio-page:not(.hidden)){background:radial-gradient(ellipse at 8% 8%,#ffb0dc99,transparent 34%),radial-gradient(ellipse at 92% 90%,#8ff2bf77,transparent 38%),linear-gradient(145deg,#51254f 0%,#a04479 52%,#356d7a 100%)!important;}
.screen:has(#quran-page:not(.hidden)){background:radial-gradient(ellipse at 85% 8%,#f2d58b99,transparent 34%),radial-gradient(ellipse at 8% 90%,#75e5c677,transparent 38%),linear-gradient(145deg,#103a3c 0%,#1b6a5b 52%,#5e6947 100%)!important;}
.screen:has(#pin-page:not(.hidden)){background:radial-gradient(ellipse at 50% 8%,#9feaff99,transparent 34%),radial-gradient(ellipse at 8% 90%,#ffad9a77,transparent 38%),linear-gradient(145deg,#172b50 0%,#326b94 52%,#5a497b 100%)!important;}
/* Breakout remains a single 2D canvas; no Three.js canvas is layered over it. */
#breakout-page #nb-canvas{position:relative!important;z-index:1!important;display:block!important;width:100%!important;height:auto!important;aspect-ratio:360/520!important;max-height:none!important;transform:none!important;}
#breakout-page .nb-controls-hint{font-size:9px;color:#a9e8f5;margin:3px 0 0!important;}
#breakout-page .nb-panel>p{display:none;}
#car-page .card{display:block!important;position:relative!important;}
#car-canvas{backface-visibility:hidden!important;will-change:auto!important;}


/* Final Car Racing correction: fixed camera, upright cars, no zoom. */
#car-page .card{display:flex!important;flex-direction:column!important;align-items:stretch!important;overflow:hidden!important;}
#car-canvas{display:block!important;position:relative!important;inset:auto!important;float:none!important;clear:both!important;width:min(100%,260px)!important;min-width:0!important;height:auto!important;aspect-ratio:340/510!important;max-height:none!important;object-fit:contain!important;object-position:center!important;margin:5px auto 8px!important;transform:none!important;animation:none!important;flex:0 0 auto!important;box-sizing:border-box!important;}
#car-page .page-head .back{background:linear-gradient(135deg,#8667dc,#5546a8)!important;color:#fff!important;border:1px solid #c9baff!important;}
#car-page button.primary{background:linear-gradient(135deg,#ffbd58,#f07843)!important;color:#392014!important;border:1px solid #ffe0a0!important;}
#car-page .car-controls button:first-child{background:linear-gradient(135deg,#5ac8fa,#2676c9)!important;color:#071f3b!important;border:1px solid #b8eaff!important;box-shadow:0 5px 13px #102b4b77!important;}
#car-page .car-controls button:last-child{background:linear-gradient(135deg,#79e6a2,#229b70)!important;color:#073b2b!important;border:1px solid #c2ffda!important;box-shadow:0 5px 13px #102b4b77!important;}
#car-page .car-controls button{font-weight:900!important;}
@media(max-height:700px){#car-canvas{width:min(100%,260px)!important;height:auto!important;aspect-ratio:340/510!important;max-height:none!important;}}

/* Final stability and contrast pass */
#app-loading-overlay{position:absolute;inset:0;z-index:9999;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:16px;background:linear-gradient(145deg,#101d3d,#39245b 55%,#75436d);color:#fff;opacity:1;visibility:visible;pointer-events:auto;transition:opacity .28s ease,visibility .28s ease}
#app-loading-overlay.is-hidden{opacity:0;visibility:hidden;pointer-events:none}
#app-loading-overlay b{font-size:14px;letter-spacing:3px}
.app-loader-orbit{width:48px;height:48px;position:relative;border:3px solid #ffffff30;border-top-color:#8effd6;border-right-color:#c59cff;border-radius:50%;animation:appSpin .72s linear infinite}
.app-loader-orbit i{position:absolute;width:7px;height:7px;border-radius:50%;background:#ffe18a;top:-4px;left:18px;box-shadow:0 0 12px #ffe18a}
@keyframes appSpin{to{transform:rotate(360deg)}}
#car-page .card{display:flex;flex-direction:column;align-items:stretch;overflow:hidden}
#car-canvas{display:block!important;position:relative!important;inset:auto!important;float:none!important;clear:both!important;width:min(100%,272px)!important;min-width:0!important;height:auto!important;aspect-ratio:2/3!important;max-height:none!important;object-fit:contain!important;object-position:center!important;margin:5px auto 8px!important;transform:none!important;animation:none!important;flex:0 0 auto!important;box-sizing:content-box!important;}
#car-page .car-controls button{background:linear-gradient(135deg,#ffe0a0,#efad67)!important;color:#392516!important;border:1px solid #fff0c4!important;box-shadow:0 5px 13px #171b2b66!important}
.screen button.primary{background:linear-gradient(110deg,#ffcf72,#ff9f68)!important;border:1px solid #ffe3aa!important;box-shadow:0 7px 17px #17152d55!important}
.screen button.secondary{background:linear-gradient(110deg,#5e70c8,#8055a8)!important;color:#fff!important;border:1px solid #c5c8ff!important;box-shadow:0 7px 17px #17152d55!important}
@media(max-height:700px){#car-canvas{width:min(100%,272px)!important;height:auto!important;aspect-ratio:2/3!important;max-height:none!important}}



/* High-contrast button palette across login and app screens.
   Adjacent controls receive different colours so none blend into page backgrounds. */
.screen button:nth-of-type(6n+1){background:linear-gradient(135deg,#ffcf70,#f18b52)!important;border:1px solid #ffe5ad!important}
.screen button:nth-of-type(6n+2){background:linear-gradient(135deg,#62c8ff,#3976d8)!important;border:1px solid #b9eaff!important}
.screen button:nth-of-type(6n+3){background:linear-gradient(135deg,#75e6a3,#239a70)!important;border:1px solid #c2ffda!important}
.screen button:nth-of-type(6n+4){background:linear-gradient(135deg,#c69aff,#8053c8)!important;border:1px solid #e0caff!important}
.screen button:nth-of-type(6n+5){background:linear-gradient(135deg,#ff9db7,#d94e78)!important;border:1px solid #ffd0df!important}
.screen button:nth-of-type(6n){background:linear-gradient(135deg,#ffe58a,#d5a52e)!important;border:1px solid #fff0b8!important}
.screen button:disabled{filter:saturate(.45);opacity:.58}



/* USER REQUEST: restrained calculator, red/grey/light-blue accents, distinct home shortcuts, 3D green Gaming Hub. */
body{
 background:
  radial-gradient(ellipse at 12% 12%,#d95c6b55,transparent 30%),
  radial-gradient(ellipse at 88% 18%,#91c9ef55,transparent 30%),
  linear-gradient(135deg,#252b38 0%,#596575 48%,#9fc8e2 100%) !important;
}
.phone{
 background:linear-gradient(140deg,#d7e0e9 0%,#9eabb9 28%,#8eb9d7 62%,#a94f60 100%) !important;
 box-shadow:0 30px 78px #10182780,inset 0 3px 5px #ffffffb8,inset 0 -10px 22px #17223555 !important;
}
.screen:has(#home-page:not(.hidden)){
 background:
  radial-gradient(ellipse at 9% 8%,#d95b6b55,transparent 34%),
  radial-gradient(ellipse at 92% 88%,#8fc8ed55,transparent 38%),
  linear-gradient(145deg,#26313f 0%,#596575 52%,#354b63 100%) !important;
}
.screen:has(#calculator-page:not(.hidden)){
 background:
  radial-gradient(ellipse at 90% 8%,#9bc9e955,transparent 34%),
  radial-gradient(ellipse at 8% 92%,#d95c6b44,transparent 36%),
  linear-gradient(145deg,#303744 0%,#687583 52%,#38516a 100%) !important;
}
/* Calm calculator keys: one neutral family, with muted red/blue accents only. */
.screen:has(#calculator-page:not(.hidden)) .calc-display{
 background:linear-gradient(145deg,#f2f6fa,#dce5ed) !important;
 color:#263443 !important;
 border:1px solid #ffffffaa;
 box-shadow:inset 0 2px 7px #26344318,0 5px 14px #17223530;
}
.screen:has(#calculator-page:not(.hidden)) .calc-key{
 background:linear-gradient(145deg,#edf2f6,#cbd5df) !important;
 color:#273443 !important;
 border:1px solid #f7fbff !important;
 box-shadow:0 4px 8px #1722352c,inset 0 1px 0 #ffffffcc !important;
}
.screen:has(#calculator-page:not(.hidden)) .calc-key.op{
 background:linear-gradient(145deg,#b9d9ee,#7faac9) !important;
 color:#17364d !important;
 border-color:#d8efff !important;
}
.screen:has(#calculator-page:not(.hidden)) .calc-key.equal{
 background:linear-gradient(145deg,#d96a78,#a93f54) !important;
 color:#fff !important;
 border-color:#f3b1ba !important;
}
.screen:has(#calculator-page:not(.hidden)) .calc-key.clear{
 background:linear-gradient(145deg,#e9b2b8,#cc7b87) !important;
 color:#542b34 !important;
 border-color:#f7d9dd !important;
}
/* Only the four requested home navigation buttons get their own contrasting backgrounds. */
#home-page .home-shortcuts>.home-shortcut:nth-child(1){
 background:linear-gradient(145deg,#587b9d,#344f70) !important;
 border:1px solid #a9d5f3 !important;
 box-shadow:0 7px 15px #10182755,inset 0 1px 0 #ffffff55,inset 0 -5px 10px #17283c55 !important;
 color:#f7fbff !important;
}
#home-page .home-shortcuts>.home-shortcut:nth-child(2){
 background:linear-gradient(145deg,#a94e60,#713747) !important;
 border:1px solid #f2a8b2 !important;
 box-shadow:0 7px 15px #10182755,inset 0 1px 0 #ffffff55,inset 0 -5px 10px #3d1c2b55 !important;
 color:#fff8f8 !important;
}
#home-page .home-shortcuts>.home-shortcut:nth-child(3){
 background:linear-gradient(145deg,#8bbbd9,#4d789a) !important;
 border:1px solid #d0edff !important;
 box-shadow:0 7px 15px #10182755,inset 0 1px 0 #ffffff77,inset 0 -5px 10px #27445e55 !important;
 color:#102b40 !important;
}
#home-page .wide-tile{
 background:linear-gradient(145deg,#45b879 0%,#16804f 48%,#075333 100%) !important;
 border:1px solid #9dffbd !important;
 color:#f2fff6 !important;
 box-shadow:0 12px 22px #061b164f,inset 0 2px 0 #ffffff70,inset 0 -7px 13px #032f1c88,0 0 18px #4eff9b26 !important;
 transform:translateZ(0);
}
#home-page .wide-tile .wide-desc{color:#dcffe8 !important;}
#home-page .wide-tile .wide-icon{filter:drop-shadow(0 4px 4px #032c1b88);}
/* Dedicated Gaming Hub screen: layered green glass/3D finish, without changing game logic. */
.screen:has(#games-page:not(.hidden)){
 background:
  radial-gradient(ellipse at 12% 5%,#65f5a866,transparent 34%),
  radial-gradient(ellipse at 90% 92%,#25a86b55,transparent 38%),
  linear-gradient(145deg,#092d25 0%,#12613f 48%,#174b3c 100%) !important;
}
.screen:has(#games-page:not(.hidden)) #games-page .tile{
 background:linear-gradient(145deg,#38a96b 0%,#167448 48%,#0b4a35 100%) !important;
 border:1px solid #9dffc0 !important;
 color:#f2fff7 !important;
 box-shadow:0 9px 17px #031b124f,inset 0 2px 0 #ffffff55,inset 0 -6px 12px #032e1d88 !important;
 transform:translateY(0);
 transition:transform .18s ease,box-shadow .18s ease,filter .18s ease;
}
.screen:has(#games-page:not(.hidden)) #games-page .tile:active{
 transform:translateY(2px) scale(.985);
 box-shadow:0 4px 9px #031b124f,inset 0 2px 5px #032e1d88 !important;
}


/* FINAL REQUEST: premium 3D login/logout buttons + dedicated order screen */
#login-page .login-actions button.primary,
#app-login-page button.primary{
  color:#17333d!important;
  background:linear-gradient(180deg,#c7fff0 0%,#63dfc5 48%,#269b9b 100%)!important;
  border:1px solid #d8fff5!important;
  border-bottom:4px solid #176b72!important;
  border-radius:16px!important;
  box-shadow:inset 0 2px 0 #ffffffcc,inset 0 -3px 0 #126c6b55,0 9px 0 #123e50,0 14px 22px #07162966!important;
  text-shadow:0 1px 0 #ffffff70;
  transform:translateY(-2px);
}
#login-page .login-actions button.primary:active,
#app-login-page button.primary:active{
  transform:translateY(4px)!important;
  box-shadow:inset 0 3px 7px #123e5044,0 3px 0 #123e50,0 6px 10px #07162955!important;
}
#home-page .logout-row{
  color:#fff!important;
  background:linear-gradient(180deg,#ff8589 0%,#e33e50 48%,#9f1836 100%)!important;
  border:1px solid #ffb4b8!important;
  border-bottom:4px solid #70142c!important;
  box-shadow:inset 0 2px 0 #ffffff77,inset 0 -3px 0 #650d2855,0 8px 0 #4c1428,0 12px 19px #07162966!important;
  transform:translateY(-2px);
}
#home-page .logout-row:active{transform:translateY(3px)!important;box-shadow:inset 0 3px 6px #4c142866,0 2px 0 #4c1428!important}
#shop-order-page .shop-order-card{margin:10px 0;padding:13px;border-radius:16px;background:linear-gradient(145deg,#ffffff22,#ffffff0b);border:1px solid #ffffff40;box-shadow:inset 0 1px 0 #ffffff25,0 9px 20px #07172d35}
#shop-order-page .shop-order-line{display:flex;align-items:center;gap:9px;padding:9px 0;border-bottom:1px solid #ffffff20;color:#fff;font-size:11px}
#shop-order-page .shop-order-line .item-main{flex:1;min-width:0}
#shop-order-page .shop-order-line small{display:block;color:#d5e1f2;margin-top:3px}
#shop-order-page .shop-order-total{display:flex;justify-content:space-between;padding:13px 0 5px;color:#fff;font-weight:900}
#shop-order-page .shop-order-action{width:100%;padding:13px;border-radius:12px;color:#103b36;background:linear-gradient(180deg,#c4ffe2,#48d7a2 58%,#15966f)!important;border:1px solid #d8ffed!important;border-bottom:4px solid #08654c!important;box-shadow:inset 0 2px 0 #ffffffaa,0 7px 0 #0b4c42,0 11px 18px #07162955!important}
#shop-order-page .shop-order-action:active{transform:translateY(3px);box-shadow:inset 0 2px 5px #063c3544,0 2px 0 #0b4c42!important}
#shop-order-page .shop-order-muted{font-size:10px;color:#d6e3f1;line-height:1.55}
#shop-order-page .shop-history-entry{padding:11px;margin:8px 0;border-radius:12px;background:#ffffff12;border:1px solid #ffffff25;color:#fff;font-size:10px}
.screen:has(#shop-order-page:not(.hidden)){background:radial-gradient(ellipse at 88% 8%,#ff9dc955,transparent 34%),linear-gradient(145deg,#251d43,#59345e 55%,#28516a)}



</style>
</head>

<body>
<div class="phone">
 <main class="screen">

  <div id="app-loading-overlay" role="status" aria-live="polite">
   <div class="app-loader-orbit"><i></i></div>
   <b>MOBILE.APP</b>
   <span style="font-size:11px;color:#d9e9ff">Loading your app…</span>
  </div>

  <div class="dynamic-island" aria-hidden="true"><span></span><i></i></div>
 <div class="topbar">
   <div class="brand">✦ MOBILE.APP</div>
   <div class="pill" id="top-time">--:--</div>
  </div>

  <section id="login-page" class="login-wrap">
   <div class="clock-panel">
    <div class="clock-face" id="clock-face">
     <span class="number" style="left:50%;top:13%">12</span>
     <span class="number" style="left:83%;top:50%">3</span>
     <span class="number" style="left:50%;top:87%">6</span>
     <span class="number" style="left:17%;top:50%">9</span>
     <div class="hand hour-hand" id="hour-hand"></div>
     <div class="hand minute-hand" id="minute-hand"></div>
     <div class="hand second-hand" id="second-hand"></div>
     <div class="clock-pin"></div>
    </div>
    <div class="time-info">
     <div class="digital-time" id="digital-time">00:00:00</div>
     <div class="digital-date" id="digital-date">Loading date...</div>
    </div>
   </div>

   <div class="login-title">Welcome</div>
   <h2 style="color:#f5fffc;margin:5px 0">Your space. Your apps.</h2>
   

   <div class="login-actions">
    <button class="primary" onclick="login()">LOGIN</button>
    <button class="secondary" onclick="guestLogin()">EXPLORE AS GUEST</button>
   </div>
   
  </section>

  <section id="app-login-page" class="hidden">
   <div class="login-wrap" style="min-height:620px">
    <div class="login-title">Sign in</div>
    <h2 style="color:#f5fffc;margin:5px 0 12px">Welcome to mobile.app</h2>
    
    <div class="card" style="width:100%;max-width:320px;text-align:left">
     <label for="app-login-email">Gmail address</label>
     <input class="field" id="app-login-email" type="email" inputmode="email" autocomplete="username" placeholder="yourname@gmail.com">
     <label for="app-login-password">mobile.app password</label>
     <input class="field" id="app-login-password" type="password" autocomplete="current-password" placeholder="Enter app password">
     
     <button class="primary" onclick="submitAppLogin()">CONTINUE</button>
     <p id="app-login-message" class="small-note" role="status" style="margin:10px 0 0"></p>
    </div>
    <button class="secondary" style="max-width:320px;margin-top:10px" onclick="showPage('login-page')">BACK</button>
   </div>
  </section>

  <section id="home-page" class="hidden">
   <div class="home-pager" id="home-pager">
    <div class="home-panel" id="home-panel-0">
     <div class="section">
      <p style="margin-bottom:5px">WELCOME BACK</p>
      <h1 id="welcome-name">Hello!</h1>
      <p>Your personal mobile space is ready.</p>
     </div>
     <div class="section tile-grid">
      <button class="tile" onclick="openPage('calculator-page')"><span class="emoji">🧮</span><span>Calculator</span></button>
      <button class="tile" onclick="openPage('password-page')"><span class="emoji">🔐</span><span>Password</span></button>
      <button class="tile" onclick="openPage('notes-page')"><span class="emoji">📝</span><span>Notes</span></button>
     </div>
     <div class="section">
      <button class="wide-tile" onclick="openPage('games-page')">
       <span class="wide-icon">🧩</span>
       <span><div class="wide-title">Gaming Hub</div><div class="wide-desc">Play, challenge yourself and enjoy your mini-games collection.</div></span>
       <span style="margin-left:auto;font-size:23px">›</span>
      </button>
     </div>
     <div class="home-shortcuts">
      <button class="home-shortcut" onclick="openPage('settings-page')"><span class="emoji">⚙️</span><b>SETTINGS</b></button>
      <button class="home-shortcut" onclick="openPage('about-page')"><span class="emoji">✨</span><b>ABOUT</b></button>
      <button class="home-shortcut" onclick="openPage('school-page')"><span class="emoji">🏫</span><b>ABOUT MY SCHOOL</b></button>
     </div>
     <button class="logout-row" onclick="logout()"><span class="emoji">🚪</span><b>LOGOUT</b><span class="logout-arrow">›</span></button>
    </div>
    <div class="home-panel" id="home-panel-1">
     <div class="home-second-heading"><span>📱</span><div><b>MORE APPS</b><small>Swipe to explore your mobile space</small></div></div>
     <div class="home-shortcuts home-shortcuts-second">
      <button class="home-shortcut" style="background:linear-gradient(145deg,#152d58,#38265e);border-color:#9bb7ff" onclick="openPage('solar-page');solarSelect('earth')"><span class="emoji">🪐</span><b>SOLAR SYSTEM</b></button>
      <button class="home-shortcut" style="background:linear-gradient(145deg,#176b67,#17436f);border-color:#8dffd1" onclick="openPage('quran-page')"><span class="emoji">📖</span><b>QURAN READER</b></button>
      <button class="home-shortcut shop-shortcut" onclick="openPage('shopping-page');shopRender()"><span class="emoji">🛍️</span><b>SHOPPING STORE</b></button>
      <button class="home-shortcut" style="background:linear-gradient(145deg,#145c69,#303b76);border-color:#8ff5e0" onclick="openPage('house-page')"><span class="emoji">🏠</span><b>HOUSE DESIGNER</b></button>
      <button class="home-shortcut weather-shortcut" onclick="openPage('weather-page');weatherLoad()"><span class="emoji">🌦️</span><b>WEATHER FORECAST</b></button>
      <button class="home-shortcut" style="background:linear-gradient(145deg,#17345f,#185c68);border-color:#8be9ff" onclick="openPage('studio-page');studioInit()"><span class="emoji">🎨</span><b>CREATIVE STUDIO</b></button>
     </div>
     <div class="section" style="margin-top:12px">
      <button class="wide-tile" style="background:linear-gradient(145deg,#1c6480,#34418a 55%,#5a438d);border:1px solid #a9eaff;box-shadow:0 7px 0 #182d5b,0 12px 22px #07152b88,inset 0 2px #ffffff66" onclick="openMyAI()">
       <span class="wide-icon">✦</span><span><div class="wide-title">My AI</div><div class="wide-desc">Open your full AI assistant</div></span><span style="margin-left:auto;font-size:23px">›</span>
      </button>
     </div>
     <div class="home-page-note">Your apps are arranged across two home screens.</div>
     <button class="logout-row" onclick="logout()"><span class="emoji">🚪</span><b>LOGOUT</b><span class="logout-arrow">›</span></button>
    </div>
   </div>
   <div class="home-pagination">
    <button type="button" class="home-arrow" id="home-prev" onclick="homeSwipeTo(0)" aria-label="Previous home screen">‹</button>
    <div class="home-dots"><button id="home-dot-0" class="home-dot active" onclick="homeSwipeTo(0)" aria-label="Home screen one"></button><button id="home-dot-1" class="home-dot" onclick="homeSwipeTo(1)" aria-label="Home screen two"></button></div>
    <button type="button" class="home-arrow" id="home-next" onclick="homeSwipeTo(1)" aria-label="Next home screen">›</button>
   </div>
  </section>

  <section id="weather-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>🌦️ Weather Forecast</h2></div>
   <div class="weather-hero">
    <div class="weather-kicker">LIVE CONDITIONS · 7 DAY OUTLOOK</div>
    <div class="weather-search"><input id="weather-city" class="field" type="search" value="Karachi" placeholder="Search city..." onkeydown="if(event.key==='Enter')weatherLoad()"><button class="weather-search-btn" onclick="weatherLoad()">SEARCH</button></div>
    <div id="weather-status" class="weather-status">Live weather powered by Open-Meteo</div>
    <div class="weather-current"><div><div id="weather-place" class="weather-place">Karachi</div><div id="weather-condition" class="weather-condition">Loading forecast...</div><div id="weather-temp" class="weather-temp">--°</div><div id="weather-range" class="weather-range">H: --°  L: --°</div></div><div id="weather-icon" class="weather-icon">🌤️</div></div>
    <div class="weather-stats"><div><small>FEELS LIKE</small><b id="weather-feels">--°</b></div><div><small>HUMIDITY</small><b id="weather-humidity">--%</b></div><div><small>WIND</small><b id="weather-wind">-- km/h</b></div><div><small>UV INDEX</small><b id="weather-uv">--</b></div></div>
    <div class="weather-extra-stats"><div><small>🌅 SUNRISE</small><b id="weather-sunrise">--:--</b></div><div><small>🌇 SUNSET</small><b id="weather-sunset">--:--</b></div><div><small>🌧️ RAIN CHANCE</small><b id="weather-rain">--%</b></div></div>
   </div>
   <div class="weather-section"><div class="weather-section-title"><h3>Next 12 hours</h3><span>HOURLY</span></div><div id="weather-hourly" class="weather-hourly"><p>Forecast will appear here.</p></div></div>
   <div class="weather-section"><div class="weather-section-title"><h3>7-day forecast</h3><span>DAILY</span></div><div id="weather-daily" class="weather-daily"><p>Forecast will appear here.</p></div></div>
   <p class="small-note">Forecast data is provided by Open-Meteo. Internet connection is required.</p>
  </section>


  <section id="house-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>🏠 House Designer</h2></div>
   <div class="hd-hero"><div class="hd-kicker">MOBILE.APP DESIGN STUDIO</div><h2>Build your dream home</h2><p>Plan rooms, arrange furniture, customize finishes and switch to an isometric 3D-style view.</p><div class="hd-stats"><div><b id="hd-room-count">0</b><span>ROOMS</span></div><div><b id="hd-item-count">0</b><span>OBJECTS</span></div><div><b id="hd-area">0</b><span>m² APPROX.</span></div></div></div>
   <div class="hd-toolbar"><button class="hd-tab active" id="hd-tab-plan" onclick="hdSetView('plan')">▦ 2D FLOOR PLAN</button><button class="hd-tab" id="hd-tab-3d" onclick="hdSetView('3d')">◇ 3D PREVIEW</button></div>
   <div class="hd-canvas-wrap"><canvas id="hd-canvas" width="900" height="620" aria-label="Interactive house plan"></canvas><div class="hd-canvas-hint" id="hd-canvas-hint">Tap an object to select · Drag to move · Pinch/zoom with controls</div></div>
   <div class="hd-controls">
    <div class="hd-panel"><div class="hd-panel-head"><h3>＋ Add rooms</h3><span>ROOM BUILDER</span></div><div class="hd-choice-grid"><button onclick="hdAddRoom('Living Room')">🛋️<b>Living</b></button><button onclick="hdAddRoom('Bedroom')">🛏️<b>Bedroom</b></button><button onclick="hdAddRoom('Kitchen')">🍳<b>Kitchen</b></button><button onclick="hdAddRoom('Bathroom')">🛁<b>Bathroom</b></button><button onclick="hdAddRoom('Dining')">🍽️<b>Dining</b></button><button onclick="hdAddRoom('Study')">📚<b>Study</b></button></div><p class="hd-help">Add a room, then drag it around the floor plan. Select a room to rename, resize or recolour it.</p></div>
    <div class="hd-panel"><div class="hd-panel-head"><h3>＋ Furniture</h3><span>PLACE OBJECTS</span></div><div class="hd-choice-grid hd-furniture-grid"><button onclick="hdAddItem('Sofa')">🛋️<b>Sofa</b></button><button onclick="hdAddItem('Bed')">🛏️<b>Bed</b></button><button onclick="hdAddItem('Table')">🪑<b>Table</b></button><button onclick="hdAddItem('Chair')">💺<b>Chair</b></button><button onclick="hdAddItem('Wardrobe')">🚪<b>Wardrobe</b></button><button onclick="hdAddItem('Plant')">🪴<b>Plant</b></button><button onclick="hdAddItem('Kitchen')">🍽️<b>Counter</b></button><button onclick="hdAddItem('Shower')">🚿<b>Shower</b></button><button onclick="hdAddItem('TV')">📺<b>TV</b></button><button onclick="hdAddItem('Lamp')">💡<b>Lamp</b></button></div></div>
    <div class="hd-panel" id="hd-selection-panel"><div class="hd-panel-head"><h3>Selected element</h3><span id="hd-selection-type">NOTHING SELECTED</span></div><div id="hd-selection-empty" class="hd-empty">Select a room or furniture item on the plan to edit it.</div><div id="hd-selection-edit" class="hidden"><label class="hd-label" for="hd-name">Name</label><input id="hd-name" class="field" maxlength="28" oninput="hdUpdateSelected('name',this.value)"><div class="hd-two-fields"><div><label class="hd-label" for="hd-width">Width (m)</label><input id="hd-width" class="field" type="number" min="0.5" max="20" step="0.5" onchange="hdUpdateSelected('w',this.value)"></div><div><label class="hd-label" for="hd-height">Length (m)</label><input id="hd-height" class="field" type="number" min="0.5" max="20" step="0.5" onchange="hdUpdateSelected('h',this.value)"></div></div><label class="hd-label" for="hd-color">Colour / finish</label><input id="hd-color" class="hd-color" type="color" value="#d8b18a" oninput="hdUpdateSelected('color',this.value)"><div class="hd-action-row"><button class="hd-action" onclick="hdRotateSelected()">↻ Rotate</button><button class="hd-action danger" onclick="hdDeleteSelected()">Delete</button></div></div></div>
    <div class="hd-panel"><div class="hd-panel-head"><h3>Doors & windows</h3><span>DETAILS</span></div><div class="hd-action-row"><button class="hd-action" onclick="hdAddOpening('Door')">🚪 Add door</button><button class="hd-action" onclick="hdAddOpening('Window')">▣ Add window</button></div><p class="hd-help">Doors and windows are visual markers you can move around the plan.</p></div>
    <div class="hd-panel"><div class="hd-panel-head"><h3>Project tools</h3><span>SAVE & EXPORT</span></div><div class="hd-action-row hd-project-actions"><button class="hd-action" onclick="hdSave()">💾 Save design</button><button class="hd-action" onclick="hdLoad()">↩ Load saved</button><button class="hd-action" onclick="hdExport()">⬇ Export image</button><button class="hd-action" onclick="hdNew()">＋ New plan</button></div><div class="hd-action-row"><button class="hd-action" onclick="hdUndo()">↶ Undo</button><button class="hd-action" onclick="hdZoom(-1)">－ Zoom out</button><button class="hd-action" onclick="hdZoom(1)">＋ Zoom in</button></div><p id="hd-status" class="hd-status" role="status">Your design is stored on this device when you save it.</p></div>
   </div>
  </section>

  <section id="shopping-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>🛍️ Shopping Store</h2></div>
   <div class="shop-hero"><div class="shop-kicker">MOBILE.APP MARKETPLACE</div><h2>Find something you love.</h2><p>Explore clothes, gadgets, shoes and everyday essentials.</p>
    <div class="shop-search-row"><input id="shop-search" class="field" type="search" placeholder="Search products..." oninput="shopRender()" aria-label="Search products"><button class="shop-cart-button" onclick="shopToggleCart()">🛒 <span id="shop-cart-count">0</span></button></div>
   </div>
   <div class="shop-categories" id="shop-categories">
    <button class="shop-category active" onclick="shopSetCategory('All',this)">All</button><button class="shop-category" onclick="shopSetCategory('Clothing',this)">Clothing</button><button class="shop-category" onclick="shopSetCategory('Shoes',this)">Shoes</button><button class="shop-category" onclick="shopSetCategory('Electronics',this)">Electronics</button><button class="shop-category" onclick="shopSetCategory('Accessories',this)">Accessories</button><button class="shop-category" onclick="shopSetCategory('Home',this)">Home</button><button class="shop-category" onclick="shopSetCategory('Beauty',this)">Beauty</button>
   </div>
   <div class="shop-section-head"><h3>Popular products</h3><span id="shop-result-count">100 items</span></div><div class="shop-grid" id="shop-products"></div>
   <div id="shop-detail" class="shop-detail hidden" aria-live="polite"></div>
   <div id="shop-cart-panel" class="shop-cart-panel hidden"><div class="shop-cart-head"><h3>Your cart</h3><button class="shop-close" onclick="shopToggleCart()">✕</button></div><div id="shop-cart-items"></div><div class="shop-total"><span>Total</span><b id="shop-total">Rs. 0</b></div><button class="primary" onclick="shopCheckout()">PLACE DEMO ORDER</button><p class="small-note">Demo store only — no real payment or order is processed.</p></div>
   <p id="shop-message" class="shop-message" role="status"></p><p class="small-note">Demo prices are shown in Pakistani rupees. Product availability and checkout are simulated.</p>
  </section>

  <section id="shop-order-page" class="hidden">
   <div class="page-head"><button class="back" onclick="openPage('shopping-page');shopRender()">‹ Back to store</button><h2>🛒 Your Orders</h2></div>
   <div class="shop-hero"><div class="shop-kicker">MOBILE.APP CHECKOUT</div><h2>Review your order</h2><p>Check your selected items, place a demo order, and view your order history here.</p></div>
   <div class="shop-order-card">
    <div class="shop-section-head"><h3>🧺 Order summary</h3><span id="shop-order-item-count">0 items</span></div>
    <div id="shop-order-cart-lines"><p class="shop-order-muted">Your cart is empty. Return to the store and add products.</p></div>
    <div class="shop-order-total"><span>Total</span><b id="shop-order-total">Rs. 0</b></div>
    <button class="shop-order-action" onclick="shopCheckout()">✓ PLACE DEMO ORDER</button>
    <p class="shop-order-muted" style="margin:10px 1px 0">Demo checkout only. No payment, delivery request, or real purchase is made.</p>
   </div>
   <div class="shop-order-card">
    <div class="shop-section-head"><h3>📦 Order history</h3><span id="shop-history-count">0 orders</span></div>
    <div id="shop-order-history"><p class="shop-order-muted">Your placed demo orders will appear here.</p></div>
   </div>
   <p id="shop-order-message" class="shop-message" role="status" aria-live="polite"></p>
  </section>

  <section id="breakout-page" class="hidden">
   <div class="page-head"><button class="back" onclick="breakoutStop();goHome()">‹ Back</button><h2>🟣 Neon Breakout</h2></div>
   <div class="nb-hero"><div class="nb-kicker">ARCADE CHALLENGE / SEASON 01</div><h2 style="font-size:24px;margin:8px 0">BREAK THE GRID.</h2><div class="nb-stats"><div class="nb-stat"><b id="nb-score">0</b><small>SCORE</small></div><div class="nb-stat"><b id="nb-lives">3</b><small>LIVES</small></div><div class="nb-stat"><b id="nb-best">0</b><small>BEST</small></div></div></div>
   <h3>⚡ ARCADE ARENA</h3><div class="nb-panel"><div class="nb-row" style="justify-content:space-between;margin:2px 0 7px"><b id="nb-level-label">LEVEL 01 / 30</b><span id="nb-status" class="nb-status">Tap START to play</span></div><div class="nb-row" style="margin-bottom:7px"><button class="nb-btn" id="nb-start" onclick="breakoutToggle()">START GAME</button><button class="nb-ghost" onclick="breakoutPause()">Ⅱ PAUSE</button><button class="nb-ghost" onclick="breakoutRestart()">↻ RESTART</button></div><canvas id="nb-canvas" width="360" height="520"></canvas><p class="nb-controls-hint" style="margin:3px 0 0;text-align:center">Move: A / D or ← / → · Touch: drag</p><div class="nb-row" style="justify-content:center;margin-top:8px"><button class="nb-ghost" onpointerdown="breakoutMove(-1)" onpointerup="breakoutMove(0)" onpointerleave="breakoutMove(0)">◀ LEFT</button><button class="nb-ghost" onpointerdown="breakoutMove(1)" onpointerup="breakoutMove(0)" onpointerleave="breakoutMove(0)">RIGHT ▶</button></div></div>
   <h3>🧩 STAGE SELECT</h3><div class="nb-panel"><div id="nb-levels" class="nb-levels"></div></div>
   
   <h3>🏆 PROGRESS</h3><div class="nb-panel"><div class="nb-row" style="justify-content:space-between"><b id="nb-progress-label">0 / 30 stages cleared</b><b id="nb-coins">0 ✦</b></div><div style="height:7px;background:#ffffff18;border-radius:20px;overflow:hidden;margin-top:9px"><div id="nb-progress" style="height:100%;width:0;background:linear-gradient(90deg,#4ce7e9,#b16cff)"></div></div></div>
  </section>
  <section id="calculator-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>Calculator</h2></div>
   <div class="calc-display" id="calc-display">0</div>
   <div class="calc-grid" id="calc-grid">
    <button class="calc-key clear" onclick="calcClear()">AC</button>
    <button class="calc-key op" onclick="calcInput('%')">%</button>
    <button class="calc-key op" onclick="calcInput('/')">÷</button>
    <button class="calc-key op" onclick="calcInput('*')">×</button>
    <button class="calc-key" onclick="calcInput('7')">7</button>
    <button class="calc-key" onclick="calcInput('8')">8</button>
    <button class="calc-key" onclick="calcInput('9')">9</button>
    <button class="calc-key op" onclick="calcInput('-')">−</button>
    <button class="calc-key" onclick="calcInput('4')">4</button>
    <button class="calc-key" onclick="calcInput('5')">5</button>
    <button class="calc-key" onclick="calcInput('6')">6</button>
    <button class="calc-key op" onclick="calcInput('+')">+</button>
    <button class="calc-key" onclick="calcInput('1')">1</button>
    <button class="calc-key" onclick="calcInput('2')">2</button>
    <button class="calc-key" onclick="calcInput('3')">3</button>
    <button class="calc-key equal" onclick="calcResult()">=</button>
    <button class="calc-key" style="grid-column:span 2" onclick="calcInput('0')">0</button>
    <button class="calc-key" onclick="calcInput('.')">.</button>
    <button class="calc-key" onclick="calcBack()">⌫</button>
   </div>
  </section>

   <section id="password-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>Password Generator</h2></div>
   <div class="card">
    <p>Create a strong random password.</p>
    <label>Password length</label>
    <input class="field" id="pass-length" type="number" min="6" max="40" value="16">
    <button class="primary" onclick="generatePassword()">GENERATE PASSWORD</button>
    <div class="output" id="password-output">Your password appears here.</div>
    <button class="secondary" onclick="copyPassword()">COPY PASSWORD</button>
   </div>
  </section>

  <section id="notes-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>My Notes</h2></div>
   <div class="card">
    <input class="field" id="note-title" placeholder="Note title">
    <textarea class="field" id="note-body" rows="5" placeholder="Write your note..."></textarea>
    <button class="primary" onclick="saveNote()">SAVE NOTE</button>
    <div id="notes-list" style="margin-top:15px"></div>
   </div>
  </section>

  <section id="games-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>Gaming Hub</h2></div>
   <p>Choose a game and enjoy your break.</p>
   <div class="tile-grid">
    <button class="tile" onclick="openPage('guess-page')"><span class="emoji">🔢</span><span>Number Guess</span></button>
    <button class="tile" onclick="openPage('typing-page')"><span class="emoji">⌨️</span><span>Typing Speed</span></button>
    <button class="tile" onclick="openPage('flappy-page')"><span class="emoji">🐦</span><span>Flappy Bird</span></button>
    <button class="tile" onclick="openPage('snake-page')"><span class="emoji">🐍</span><span>Snake</span></button>
    <button class="tile" onclick="openPage('car-page')"><span class="emoji">🏎️</span><span>Car Racing</span></button>
    <button class="tile" style="background:linear-gradient(145deg,#4c368c,#192d59);border-color:#c4a4ff" onclick="openPage('breakout-page');breakoutInit()"><span class="emoji">🟣</span><span>Neon Breakout</span></button>
   </div>
  </section>

  <section id="guess-page" class="hidden">
   <div class="page-head"><button class="back" onclick="openPage('games-page')">‹ Games</button><h2>Number Guess</h2></div>
   <div class="card">
    <canvas id="guess-3d" class="mini-3d-game" aria-hidden="true"></canvas>
    <p>Guess the secret number from 1 to 100. You have 10 chances.</p>
    <input class="field" id="guess-input" type="number" min="1" max="100" placeholder="Your guess">
    <button class="primary" onclick="makeGuess()">GUESS</button>
    <p id="guess-message">10 chances remaining.</p>
    <button class="secondary" onclick="resetGuess()">RESTART GAME</button>
   </div>
  </section>

  <section id="typing-page" class="hidden">
   <div class="page-head"><button class="back" onclick="openPage('games-page')">‹ Games</button><h2>Typing Speed</h2></div>
   <div class="card">
    <canvas id="typing-3d" class="mini-3d-game" aria-hidden="true"></canvas>
    <p>Type the paragraph accurately before the 60-second timer ends.</p>
    <div id="typing-sentence">Press START to get a random paragraph.</div>
    <div class="typing-stats">
     <div class="typing-stat"><b id="typing-time">60</b><span>SECONDS LEFT</span></div>
     <div class="typing-stat"><b id="typing-live-wpm">0</b><span>LIVE WPM</span></div>
    </div>
    <textarea class="field" id="typing-input" rows="4" placeholder="Press START, then type here..." disabled></textarea>
    <button class="primary" id="typing-start-button" onclick="startTyping()">START NEW TEST</button>
    <div id="typing-results" class="hidden">
     <div class="typing-stats">
      <div class="typing-stat"><b id="typing-final-wpm">0</b><span>WORDS PER MINUTE</span></div>
      <div class="typing-stat"><b id="typing-accuracy">0%</b><span>ACCURACY</span></div>
      <div class="typing-stat"><b id="typing-correct">0</b><span>CORRECT CHARACTERS</span></div>
      <div class="typing-stat"><b id="typing-mistakes">0</b><span>MISTAKES</span></div>
     </div>
     <p id="typing-result"></p>
     <button class="secondary" onclick="startTyping()">TRY ANOTHER PARAGRAPH</button>
    </div>
   </div>
  </section>

  <section id="flappy-page" class="hidden">
   <div class="page-head"><button class="back" onclick="openPage('games-page')">‹ Games</button><h2>Flappy Bird</h2></div>
   <div class="card">
    <p>Tap the game area to flap and avoid the obstacles.</p>
    <button class="primary" onclick="startFlappy()">PLAY / RESTART</button>
    <canvas id="flappy-canvas" class="game-canvas" width="360" height="460"></canvas>
        <p id="flappy-score">Score: 0</p>
   </div>
  </section>

  <section id="snake-page" class="hidden">
   <div class="page-head"><button class="back" onclick="openPage('games-page')">‹ Games</button><h2>Snake</h2></div>
   <div class="card">
    <p>Collect the glowing fruit. Avoid the walls and your tail.</p>
    <button class="primary" onclick="startSnake()">PLAY / RESTART</button>
    <canvas id="snake-canvas" class="game-canvas" width="288" height="288"></canvas>
    <div id="snake-controls">
     <button class="empty-control" aria-hidden="true"> </button>
     <button onclick="snakeDirection(0,-1)">⬆️</button>
     <button class="empty-control" aria-hidden="true"> </button>
     <button onclick="snakeDirection(-1,0)">⬅️</button>
     <button onclick="snakeDirection(0,1)">⬇️</button>
     <button onclick="snakeDirection(1,0)">➡️</button>
    </div>
    <p id="snake-score">Score: 0</p>
   </div>
  </section>

  <section id="car-page" class="hidden">
   <div class="page-head"><button class="back" onclick="openPage('games-page')">‹ Games</button><h2>Car Racing</h2></div>
   <div class="card">
    <p>Swipe left or right to change lanes. Avoid the traffic!</p>
    <div class="car-score">
     <div><b id="car-score">0</b><span>SCORE</span></div>
     <div><b id="car-level">1</b><span>LEVEL</span></div>
     <div><b id="car-speed">1x</b><span>SPEED</span></div>
    </div>
    <button class="primary" style="margin-top:4px" onclick="startCarGame()">PLAY / RESTART</button>
    <canvas id="car-canvas" width="340" height="510"></canvas>
    <div class="car-controls">
     <button onclick="moveCar(-1)">⬅ LEFT</button>
     <button onclick="moveCar(1)">RIGHT ➡</button>
    </div>
        <p id="car-message" class="small-note">Use swipe, arrow keys or A/D to drive.</p>
   </div>
  </section>

  <section id="settings-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>Settings</h2></div>
   <div class="card">
    <label>Your name</label>
    <input class="field" id="setting-name" placeholder="Enter your name">
    <label>Set a PIN (optional)</label>
    <input class="field" id="setting-pin" type="password" maxlength="8" placeholder="Create a PIN">
    <button class="primary" onclick="saveSettings()">SAVE SETTINGS</button>
    <p class="small-note">Your notes and settings are saved on this device.</p>
   </div>
  </section>

  <section id="about-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>About</h2></div>
   <div class="card">
    <h2>✦ mobile.app</h2>
    <p>A personal mini-app space with everyday tools, notes and games.</p>
    <p>Designed with a colorful premium interface and made to work without an AI API.</p>
    <div style="margin-top:18px;padding:13px;border-radius:14px;background:#ffffff15">
     <p style="margin-bottom:8px"><b>Version:</b> 1.0</p>
     <p style="margin-bottom:0"><b>Made by:</b> Mustafa &amp; Kashan</p>
    </div>
   </div>
  </section>

  <section id="school-page" class="hidden school-page" style="--school-bg:url(1000015111.jpg)">
   <div class="school-overlay">
    <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>About My School</h2></div>
    <div class="school-menu">
     <button class="school-option history-option" onclick="openPage('school-history-page')">📚 &nbsp; History of UPSS <span>›</span></button>
     <button class="school-option mission-option" onclick="openPage('school-mission-page')">🌟 &nbsp; Mission of UPSS <span>›</span></button>
    </div>
   </div>
  </section>

  <section id="school-history-page" class="hidden school-detail history-detail">
   <div class="page-head"><button class="back" onclick="openPage('school-page')">‹ School</button><h2>History of UPSS</h2></div>
   <div class="school-text-card">
    <p>Usman Public School System (UPSS) began its educational journey in 1989. It was established with the aim of providing quality education while keeping Islamic values and character development at the heart of learning.</p>
    <p>From its beginning, the school system has focused on developing students academically, morally and socially. Its educational approach encourages discipline, responsibility, respect and a strong sense of purpose.</p>
    <p>Over the years, UPSS has grown beyond its first campus and expanded its educational work through campuses in Karachi. This growth has helped the school system reach more families and provide learning opportunities to a wider community.</p>
    <p>UPSS places importance on combining contemporary education with Islamic teachings. Along with classroom learning, students are encouraged to build good character, explore knowledge and understand their responsibilities towards society.</p>
    <p>Today, the journey of UPSS continues with an emphasis on education, values and the development of future generations. Its history reflects a continuing effort to prepare students to contribute positively to the Muslim Ummah and the wider world.</p>
   </div>
  </section>

  <section id="school-mission-page" class="hidden school-detail mission-detail">
   <div class="page-head"><button class="back" onclick="openPage('school-page')">‹ School</button><h2>Mission of UPSS</h2></div>
   <div class="school-text-card">
    <h3>Mission</h3>
    <p>To motivate the students in becoming future leaders capable of providing guidance to the Muslim Ummah in all spheres of life and lead the contemporary world in accordance with the teachings of Islam.</p>
    <h3>Vision</h3>
    <p>Nurturing students in becoming future leaders.</p>
    <h3>Core Values</h3>
    <ol>
     <li>Taqwa</li>
     <li>Following Prophet Muhammad (SAW) as a role model</li>
     <li>Research &amp; Explore</li>
     <li>Service of Mankind</li>
     <li>Enjoining Good and Forbidding Evil</li>
     <li>Protection of Ideology of Pakistan</li>
    </ol>
   </div>
  </section>


  <section id="solar-page" class="hidden">
   <div class="page-head"><button class="back" onclick="solarStop();goHome()">‹ Back</button><h2>🪐 Solar Explorer</h2></div>
   <div class="solar-hero">
    <div class="solar-kicker">SPACE OBSERVATORY · INTERACTIVE PLANET GUIDE</div>
    <h2>Explore our Solar System.</h2>
    <p>Watch the planets orbit the Sun, select a world and discover its atmosphere, moons and remarkable facts.</p>
    <div class="solar-stage" aria-label="Animated solar system model">
     <div class="solar-system">
      <div class="solar-sun" title="Sun"></div>
      <div class="solar-orbit o1"><span class="solar-body"></span></div><div class="solar-orbit o2"><span class="solar-body"></span></div>
      <div class="solar-orbit o3"><span class="solar-body"></span></div><div class="solar-orbit o4"><span class="solar-body"></span></div>
      <div class="solar-orbit o5"><span class="solar-body"></span></div><div class="solar-orbit o6"><span class="solar-body"></span></div>
      <div class="solar-orbit o7"><span class="solar-body"></span></div><div class="solar-orbit o8"><span class="solar-body"></span></div>
     </div>
     <div class="solar-stage-label">SCHEMATIC ORBITS · NOT TO SCALE</div>
    </div>
    <div class="solar-toolbar">
     <button class="solar-tool active" id="solar-motion-btn" onclick="solarToggleMotion()">Ⅱ PAUSE ORBITS</button>
     <button class="solar-tool" onclick="solarSelect('sun')">☀ EXPLORE SUN</button>
     <button class="solar-tool" onclick="solarSelect('pluto')">PLUTO</button>
    </div>
   </div>
   <h3 class="solar-section-title">SELECT A PLANET</h3>
   <div class="solar-planet-list">
    <button class="solar-pick" id="solar-pick-mercury" onclick="solarSelect('mercury')"><span class="dot" style="background:radial-gradient(circle at 30% 25%,#ddd,#777)"></span>Mercury</button>
    <button class="solar-pick" id="solar-pick-venus" onclick="solarSelect('venus')"><span class="dot" style="background:radial-gradient(circle at 30% 25%,#fff0b0,#bd743c)"></span>Venus</button>
    <button class="solar-pick" id="solar-pick-earth" onclick="solarSelect('earth')"><span class="dot" style="background:radial-gradient(circle at 30% 25%,#c4f2ff,#2687c7)"></span>Earth</button>
    <button class="solar-pick" id="solar-pick-mars" onclick="solarSelect('mars')"><span class="dot" style="background:radial-gradient(circle at 30% 25%,#ffd1a1,#b84b2b)"></span>Mars</button>
    <button class="solar-pick" id="solar-pick-jupiter" onclick="solarSelect('jupiter')"><span class="dot" style="background:radial-gradient(circle at 30% 25%,#fff0c6,#d99b5d)"></span>Jupiter</button>
    <button class="solar-pick" id="solar-pick-saturn" onclick="solarSelect('saturn')"><span class="dot" style="background:radial-gradient(circle at 30% 25%,#fff1c8,#c89b62);outline:3px solid #d9c18a88;outline-offset:1px"></span>Saturn</button>
    <button class="solar-pick" id="solar-pick-uranus" onclick="solarSelect('uranus')"><span class="dot" style="background:radial-gradient(circle at 30% 25%,#d7ffff,#77cbd1)"></span>Uranus</button>
    <button class="solar-pick" id="solar-pick-neptune" onclick="solarSelect('neptune')"><span class="dot" style="background:radial-gradient(circle at 30% 25%,#b6d9ff,#3155a2)"></span>Neptune</button>
   </div>
   <div class="solar-detail">
    <div class="solar-detail-top"><div class="solar-detail-orb" id="solar-detail-orb"></div><div><small id="solar-detail-type">PLANET</small><h3 id="solar-detail-name">Earth</h3><small id="solar-detail-distance">1 AU FROM THE SUN</small></div></div>
    <p id="solar-detail-description">Earth is our home world, with liquid-water oceans and a nitrogen- and oxygen-rich atmosphere.</p>
    <div class="solar-facts">
     <div class="solar-fact"><b id="solar-fact-year">365.25 days</b><span>ORBITAL PERIOD</span></div>
     <div class="solar-fact"><b id="solar-fact-day">24 hours</b><span>ROTATION PERIOD</span></div>
     <div class="solar-fact"><b id="solar-fact-size">12,742 km</b><span>MEAN DIAMETER</span></div>
     <div class="solar-fact"><b id="solar-fact-temp">15°C</b><span>AVERAGE TEMPERATURE</span></div>
    </div>
    <h4 class="solar-section-title">NOTABLE MOONS</h4><div class="solar-moon-list" id="solar-moons"><span class="solar-moon-chip">Moon</span></div>
   </div>
   <p class="solar-note">Distances and sizes are approximate reference values. The animated orbital layout is a visual model, not a scale representation of real distances or orbital speeds. Planet surface maps: Solar System Scope (CC BY 4.0).</p>
  </section>


  <section id="studio-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>🎨 Creative Studio</h2></div>
   <div class="studio-hero">
    <div class="studio-kicker">MOBILE.APP CREATIVE SPACE</div>
    <h2>Turn an idea into art.</h2>
    <p>Draw freely, sketch shapes, choose colours and save your artwork as an image.</p>
    <div class="studio-stats"><span><b>01</b> CREATE</span><span><b>02</b> CUSTOMIZE</span><span><b>03</b> EXPORT</span></div>
   </div>
   <div class="studio-toolbar">
    <button class="studio-tool active" data-studio-tool="pen" onclick="studioSetTool('pen',this)">✏️ Pen</button>
    <button class="studio-tool" data-studio-tool="line" onclick="studioSetTool('line',this)">／ Line</button>
    <button class="studio-tool" data-studio-tool="rect" onclick="studioSetTool('rect',this)">▱ Box</button>
    <button class="studio-tool" data-studio-tool="circle" onclick="studioSetTool('circle',this)">◯ Circle</button>
    <button class="studio-tool" data-studio-tool="triangle" onclick="studioSetTool('triangle',this)">△ Triangle</button>
    <button class="studio-tool" data-studio-tool="star" onclick="studioSetTool('star',this)">☆ Star</button>
    <button class="studio-tool" data-studio-tool="eraser" onclick="studioSetTool('eraser',this)">⌫ Eraser</button>
   </div>
   <div class="studio-board-wrap">
    <div class="studio-board-head"><b>YOUR CANVAS</b><span id="studio-status">Ready to create</span></div>
    <canvas id="studio-canvas" width="900" height="650" aria-label="Drawing canvas"></canvas>
   </div>
   <div class="studio-panel">
    <div class="studio-panel-title">Brush &amp; colour</div>
    <div class="studio-controls-grid">
     <label class="studio-control">Brush colour<input id="studio-color" type="color" value="#26334a" oninput="studioUpdateColor()"></label>
     <label class="studio-control">Brush size <b id="studio-size-label">8 px</b><input id="studio-size" type="range" min="1" max="48" value="8" oninput="studioUpdateSize(this.value)"></label>
    </div>
    <div class="studio-swatches" aria-label="Colour palette">
     <button style="--swatch:#26334a" onclick="studioChooseColor('#26334a')" aria-label="Ink"></button>
     <button style="--swatch:#e05268" onclick="studioChooseColor('#e05268')" aria-label="Coral"></button>
     <button style="--swatch:#f39b45" onclick="studioChooseColor('#f39b45')" aria-label="Orange"></button>
     <button style="--swatch:#f1cc58" onclick="studioChooseColor('#f1cc58')" aria-label="Yellow"></button>
     <button style="--swatch:#4caf91" onclick="studioChooseColor('#4caf91')" aria-label="Green"></button>
     <button style="--swatch:#4d9bd8" onclick="studioChooseColor('#4d9bd8')" aria-label="Blue"></button>
     <button style="--swatch:#8a69c9" onclick="studioChooseColor('#8a69c9')" aria-label="Purple"></button>
     <button style="--swatch:#ffffff" onclick="studioChooseColor('#ffffff')" aria-label="White"></button>
    </div>
   </div>
   <div class="studio-panel">
    <div class="studio-panel-title">Canvas background</div>
    <div class="studio-backgrounds">
     <button class="studio-bg-choice active" onclick="studioSetBackground('#ffffff',this)">White</button>
     <button class="studio-bg-choice" onclick="studioSetBackground('#fff4e7',this)">Warm</button>
     <button class="studio-bg-choice" onclick="studioSetBackground('#eaf4ff',this)">Sky</button>
     <button class="studio-bg-choice" onclick="studioSetBackground('#20283a',this)">Night</button>
    </div>
   </div>
   <div class="studio-panel">
    <div class="studio-panel-title">More creative tools</div>
    <div class="studio-extra-tools">
     <button onclick="studioAddText()">＋ Add text</button>
     <button onclick="studioToggleGrid()">▦ Toggle grid</button>
     <button onclick="studioSetStatus('Double-click any outlined shape to fill it')">▰ Double-click fill</button>
     <button onclick="studioMirror()">⇋ Mirror canvas</button>
    </div>
   </div>
   <div class="studio-actions">
    <button onclick="studioUndo()">↶ Undo</button>
    <button onclick="studioRedo()">↷ Redo</button>
    <button onclick="studioClear()">Clear</button>
    <button class="studio-save" onclick="studioDownload()">⬇ Save artwork</button>
   </div>
   <p class="studio-footnote">Your drawing stays in this session. Choose “Save artwork” to export a PNG image to your device.</p>
  </section>

  <section id="quran-page" class="hidden">
   <div class="page-head"><button class="back" onclick="goHome()">‹ Back</button><h2>📖 Quran Reader &amp; Player</h2></div>
   <div class="quran-panel">
    <label for="quran-surah">Surah</label>
    <select class="quran-control" id="quran-surah" onchange="loadQuranSurah()"><option>Loading surah list...</option></select>
    <label for="quran-translation">Translation</label>
    <select class="quran-control" id="quran-translation" onchange="loadQuranSurah()">
     <option value="">None</option>
     <option value="en.sahih" selected>English (Sahih International)</option>
     <option value="ur.jalandhry">Urdu (Jalandhry)</option>
     <option value="ur.maududi">Urdu (Maududi)</option>
     <option value="hi.hindi">Hindi</option>
     <option value="id.indonesian">Indonesian</option>
     <option value="tr.diyanet">Turkish</option>
    </select>
    <label for="quran-reciter">Reciter</label>
    <select class="quran-control" id="quran-reciter" onchange="updateQuranFullAudio()">
     <option value="https://server8.mp3quran.net/afs/{n}.mp3">Mishary Alafasy</option>
     <option value="https://server7.mp3quran.net/basit/{n}.mp3">Abdul Basit (Murattal)</option>
     <option value="https://server11.mp3quran.net/sds/{n}.mp3">Abdurrahman As-Sudais</option>
     <option value="https://server7.mp3quran.net/shur/{n}.mp3">Saud Ash-Shuraim</option>
     <option value="https://server12.mp3quran.net/maher/{n}.mp3">Maher Al-Muaiqly</option>
    </select>
    <label for="quran-font-size">Arabic font size: <span id="quran-font-label">2.0</span> rem</label>
    <input class="quran-range" id="quran-font-size" type="range" min="1.2" max="3.5" step="0.1" value="2" oninput="changeQuranFont(this.value)">
    <label style="display:flex;align-items:center;gap:8px"><input id="quran-ayah-audio" type="checkbox" onchange="toggleQuranAyahAudio()"> Show audio player for each ayah</label>
   </div>
   <div class="quran-panel">
    <h3 id="quran-surah-heading">Choose a Surah</h3>
    <p id="quran-surah-meta" class="quran-meta"></p>
    <h3 style="margin-top:12px">🎧 Listen to the full surah</h3>
    <audio id="quran-full-audio" controls preload="none" style="width:100%"></audio>
    <p id="quran-status" class="quran-status" role="status">Loading Quran data...</p>
   </div>
   <h3>📜 Read</h3>
   <div id="quran-content" class="quran-panel"><p>Surah text will appear here.</p></div>
   <p class="small-note">Text and translations: api.alquran.cloud · Audio: mp3quran.net / islamic.network</p>
  </section>



  <section id="pin-page" class="hidden">
   <div class="login-wrap" style="min-height:650px">
    <h1>Welcome back</h1>
    <p>Enter your PIN to continue.</p>
    <input class="field" id="pin-entry" type="password" placeholder="Enter PIN">
    <button class="primary" onclick="unlockApp()">UNLOCK</button>
    <p id="pin-message"></p>
   </div>
  </section>

 </main>
</div>
"""
APP += r"""
<script>
// ===============================
// MOBILE.APP - MAIN JAVASCRIPT
// ===============================
(function(){
  const hideLoader=()=>{
    const loader=document.getElementById("app-loading-overlay");
    if(loader) setTimeout(()=>loader.classList.add("is-hidden"),850);
  };
  if(document.readyState==="loading") document.addEventListener("DOMContentLoaded",hideLoader,{once:true});
  else hideLoader();
  window.addEventListener("load",hideLoader,{once:true});
})();

const $ = id => document.getElementById(id);

const store = {
  get(key, fallback) {
    try {
      const value = localStorage.getItem(key);
      return value === null ? fallback : JSON.parse(value);
    } catch (e) {
      return fallback;
    }
  },
  set(key, value) {
    try {
      localStorage.setItem(key, JSON.stringify(value));
    } catch (e) {}
  }
};
let userName = store.get("mobile_name", "Guest");
let appPin = store.get("mobile_pin", "");
let isGuest = false;
let calcExpression = "";
let secretNumber = 0;
let guessCount = 0;
let guessFinished = false;let typingStarted = false;
let typingStartTime = 0;
let typingTimer = null;
let typingSeconds = 60;
let typingText = "";
let typingUsed = [];

let flappyTimer = null;
let flappyRunning = false;
let flappyBird = null;
let flappyPipes = [];
let flappyScore = 0;

let snakeFrame = null;
let snakeRunning = false;
let snakeBody = [];
let snakePreviousBody = [];
let snakeFood = null;
let snakeDir = {x:1,y:0};
let snakeNextDir = {x:1,y:0};
let snakePoints = 0;
let snakeLastTime = 0;
let snakeAccumulator = 0;
let snakeStep = 125;
let snakeTouchStart = null;

let carFrame = null;
let carRunning = false;
let carLastTime = 0;
let carPlayerLane = 1;
let carPlayerX = 0;
let carObstacles = [];
let carScore = 0;
let carSpeed = 155;
let carSpawnTimer = 0;
let carRoadOffset = 0;
let carTouchStart = null;

function updateClock() {
  const now = new Date();
  const h = now.getHours();
  const m = now.getMinutes();
  const s = now.getSeconds();

  const hour = (h % 12) * 30 + m * 0.5;
  const minute = m * 6 + s * 0.1;
  const second = s * 6;

  if ($("hour-hand"))
    $("hour-hand").style.transform =
      `translateX(-50%) rotate(${hour}deg)`;

  if ($("minute-hand"))
    $("minute-hand").style.transform =
      `translateX(-50%) rotate(${minute}deg)`;

  if ($("second-hand"))
    $("second-hand").style.transform =
      `translateX(-50%) rotate(${second}deg)`;

  const time = now.toLocaleTimeString([], {
    hour:"2-digit", minute:"2-digit", second:"2-digit"
  });

  if ($("digital-time")) $("digital-time").textContent = time;

  if ($("top-time")) {
    $("top-time").textContent = now.toLocaleTimeString([], {
      hour:"2-digit", minute:"2-digit"
    });
  }

  if ($("digital-date")) {
    $("digital-date").textContent = now.toLocaleDateString([], {
      weekday:"long", day:"numeric", month:"long", year:"numeric"
    });
  }
}

updateClock();
setInterval(updateClock, 1000);

function openMyAI(){ if(typeof window.mobileAppOpenAI==="function") window.mobileAppOpenAI(); }

// PAGE NAVIGATION

const pages = [
  "login-page","app-login-page","home-page","calculator-page","password-page",
  "notes-page","games-page","guess-page","typing-page",
  "flappy-page","snake-page","car-page","settings-page",
  "about-page","school-page","school-history-page","school-mission-page","breakout-page","solar-page","quran-page","shopping-page","shop-order-page","house-page","weather-page","pin-page", "studio-page"];

function stopFlappy() {
  if (flappyTimer !== null) {
    clearInterval(flappyTimer);
    flappyTimer = null;
  }
  flappyRunning = false;
}

function stopSnake() {
  if (snakeFrame !== null) {
    cancelAnimationFrame(snakeFrame);
    snakeFrame = null;
  }
  snakeRunning = false;
}

function stopTyping() {
  if (typingTimer !== null) {
    clearInterval(typingTimer);
    typingTimer = null;
  }
  typingStarted = false;
}

function stopCar() {
  if (carFrame !== null) {
    cancelAnimationFrame(carFrame);
    carFrame = null;
  }
  carRunning = false;
}

function showPage(id) {
  stopFlappy();
  stopSnake();
  stopTyping();
  stopCar();

  pages.forEach(page => {
    const el = $(page);
    if (el) el.classList.toggle("hidden", page !== id);
  });

  if (id === "home-page") homeSwipeTo(0);
  if (id === "notes-page") renderNotes();

  if (id === "settings-page") {
    $("setting-name").value = store.get("mobile_name", "Guest");
    $("setting-pin").value = "";
  }

  if (id === "flappy-page") drawFlappy();
  if (id === "snake-page") drawSnake();
  if (id === "car-page") drawCar();
}

function openPage(id) {
  showPage(id);
  if (id === "quran-page") initQuranReader();
  if (id === "house-page") hdInit();
}

function goHome() {
  if (appPin && !isGuest) {
    showPage("pin-page");
    return;
  }
  showPage("home-page");
}


// HOME SCREEN SWIPE CONTROLS
let homeScreenIndex = 0;
function homeSwipeTo(index) {
  homeScreenIndex = Math.max(0, Math.min(1, Number(index) || 0));
  const pager = $("home-pager");
  if (pager) pager.style.transform = `translateX(-${homeScreenIndex * 50}%)`;
  [0,1].forEach(i => {
    const dot = $("home-dot-" + i);
    if (dot) dot.classList.toggle("active", i === homeScreenIndex);
  });
  const prev = $("home-prev"), next = $("home-next");
  if (prev) prev.style.opacity = homeScreenIndex === 0 ? ".45" : "1";
  if (next) next.style.opacity = homeScreenIndex === 1 ? ".45" : "1";
}
(function initHomeSwipe(){
  const pager = $("home-pager");
  if (!pager) return;
  let startX = 0, startY = 0, tracking = false;
  pager.addEventListener("touchstart", e => {
    if (!e.touches || e.touches.length !== 1) return;
    startX = e.touches[0].clientX; startY = e.touches[0].clientY; tracking = true;
  }, {passive:true});
  pager.addEventListener("touchend", e => {
    if (!tracking || !e.changedTouches || !e.changedTouches.length) return;
    const dx = e.changedTouches[0].clientX - startX;
    const dy = e.changedTouches[0].clientY - startY;
    if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy) * 1.25) homeSwipeTo(dx < 0 ? 1 : 0);
    tracking = false;
  }, {passive:true});
  let pointerX = 0, pointerY = 0, pointerDown = false;
  pager.addEventListener("pointerdown", e => {
    if (e.pointerType === "mouse" && e.button === 0) { pointerX=e.clientX; pointerY=e.clientY; pointerDown=true; }
  });
  pager.addEventListener("pointerup", e => {
    if (!pointerDown) return;
    const dx=e.clientX-pointerX, dy=e.clientY-pointerY;
    if (Math.abs(dx)>55 && Math.abs(dx)>Math.abs(dy)*1.25) homeSwipeTo(dx<0?1:0);
    pointerDown=false;
  });
  pager.addEventListener("pointercancel",()=>{pointerDown=false;});
  document.addEventListener("keydown", e => {
    if (!$("home-page") || $("home-page").classList.contains("hidden")) return;
    if (e.key === "ArrowRight") homeSwipeTo(1);
    if (e.key === "ArrowLeft") homeSwipeTo(0);
  });
  homeSwipeTo(0);
})();

// LIVE WEATHER FORECAST — Open-Meteo (no API key required)
const weatherCodeInfo = code => {
  if (code === 0) return ["Clear sky","☀️"];
  if ([1,2].includes(code)) return ["Mainly clear","🌤️"];
  if (code === 3) return ["Overcast","☁️"];
  if ([45,48].includes(code)) return ["Foggy","🌫️"];
  if ([51,53,55,56,57].includes(code)) return ["Drizzle","🌦️"];
  if ([61,63,65,66,67,80,81,82].includes(code)) return ["Rain showers","🌧️"];
  if ([71,73,75,77,85,86].includes(code)) return ["Snow","❄️"];
  if ([95,96,99].includes(code)) return ["Thunderstorm","⛈️"];
  return ["Variable conditions","🌥️"];
};
function weatherSetText(id, value) { const el=$(id); if(el) el.textContent=value; }
async function weatherLoad(){
  const input=$("weather-city"), status=$("weather-status");
  const city=(input?.value||"Karachi").trim();
  if(!city){if(status)status.textContent="Enter a city name first.";return;}
  if(status)status.textContent="Searching location and loading live forecast…";
  const hourly=$("weather-hourly"), daily=$("weather-daily");
  try{
    const geoUrl="https://geocoding-api.open-meteo.com/v1/search?name="+encodeURIComponent(city)+"&count=1&language=en&format=json";
    const geoResponse=await fetch(geoUrl);
    if(!geoResponse.ok)throw new Error("Could not search for this city.");
    const geo=await geoResponse.json();
    if(!geo.results?.length)throw new Error("City not found. Check the spelling and try again.");
    const place=geo.results[0];
    const params=new URLSearchParams({latitude:place.latitude,longitude:place.longitude,current:"temperature_2m,relative_humidity_2m,apparent_temperature,is_day,precipitation,weather_code,wind_speed_10m",hourly:"temperature_2m,precipitation_probability,weather_code",daily:"weather_code,temperature_2m_max,temperature_2m_min,sunrise,sunset,uv_index_max",timezone:"auto",forecast_days:"7"});
    const response=await fetch("https://api.open-meteo.com/v1/forecast?"+params.toString());
    if(!response.ok)throw new Error("Weather service is temporarily unavailable.");
    const data=await response.json(), current=data.current, d=data.daily;
    const [condition,icon]=weatherCodeInfo(current.weather_code);
    weatherSetText("weather-place",[place.name,place.admin1,place.country].filter(Boolean).join(", "));
    weatherSetText("weather-condition",condition);
    weatherSetText("weather-temp",Math.round(current.temperature_2m)+"°");
    weatherSetText("weather-range","H: "+Math.round(d.temperature_2m_max[0])+"°  L: "+Math.round(d.temperature_2m_min[0])+"°");
    weatherSetText("weather-feels",Math.round(current.apparent_temperature)+"°");
    weatherSetText("weather-humidity",current.relative_humidity_2m+"%");
    weatherSetText("weather-wind",Math.round(current.wind_speed_10m)+" km/h");
    weatherSetText("weather-uv",d.uv_index_max?.[0] ?? "--");
    weatherSetText("weather-sunrise",d.sunrise?.[0] ? new Date(d.sunrise[0]).toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"}) : "--:--");
    weatherSetText("weather-sunset",d.sunset?.[0] ? new Date(d.sunset[0]).toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"}) : "--:--");
    const nextRain=(data.hourly.precipitation_probability||[]).find((value,i)=>new Date(data.hourly.time[i]).getTime()>=new Date(current.time).getTime());
    weatherSetText("weather-rain",nextRain==null ? "--%" : nextRain+"%");
    weatherSetText("weather-icon",icon);
    if(status)status.textContent="Updated just now · Local time: "+new Date(current.time).toLocaleTimeString([], {hour:"2-digit",minute:"2-digit"});
    if(hourly){
      const now=new Date(current.time).getTime();
      let indexes=data.hourly.time.map((t,i)=>({t,i})).filter(x=>new Date(x.t).getTime()>=now).slice(0,12);
      hourly.innerHTML=indexes.map(({t,i})=>{const [label,ico]=weatherCodeInfo(data.hourly.weather_code[i]);return `<div class="weather-hour"><small>${new Date(t).toLocaleTimeString([], {hour:"numeric"})}</small><span title="${label}">${ico}</span><b>${Math.round(data.hourly.temperature_2m[i])}°</b><small>💧 ${data.hourly.precipitation_probability?.[i]??0}%</small></div>`;}).join("")||"<p>No hourly forecast available.</p>";
    }
    if(daily){
      daily.innerHTML=d.time.map((day,i)=>{const [label,ico]=weatherCodeInfo(d.weather_code[i]);const date=new Date(day+"T12:00:00");const dayName=i===0?"Today":date.toLocaleDateString([], {weekday:"short"});return `<div class="weather-day"><b>${dayName}</b><span title="${label}">${ico}</span><small>${Math.round(d.temperature_2m_min[i])}°</small><strong>${Math.round(d.temperature_2m_max[i])}°</strong></div>`;}).join("");
    }
  }catch(error){
    if(status)status.textContent="Weather could not be loaded.";
    if(hourly)hourly.innerHTML='<div class="weather-error">'+String(error.message||error).replace(/[<>]/g,"")+"</div>";
    if(daily)daily.innerHTML="";
  }
}

// LOGIN / LOGOUT

function login() {
  isGuest = false;
  $("app-login-email").value = "";
  $("app-login-password").value = "";
  $("app-login-message").textContent = "";
  showPage("app-login-page");
}

function submitAppLogin() {
  const email = $("app-login-email").value.trim();
  const password = $("app-login-password").value;
  const emailPattern = /^[A-Z0-9._%+-]+@gmail\.com$/i;
  const message = $("app-login-message");

  if (!emailPattern.test(email)) {
    message.textContent = "Please enter a valid address ending in @gmail.com.";
    return;
  }
  if (!password.trim()) {
    message.textContent = "Please enter your mobile.app password.";
    return;
  }

  // This is a local demo sign-in only. Never save or transmit the password.
  userName = email.split("@")[0];
  isGuest = false;
  $("app-login-password").value = "";
  message.textContent = "";

  if (appPin) {
    showPage("pin-page");
    return;
  }
  enterHome();
}

function guestLogin() {
  isGuest = true;
  userName = "Guest";
  enterHome();
}

function enterHome() {
  $("welcome-name").textContent = "Hello, " + userName + "!";
  showPage("home-page");
}

function logout() {
  stopFlappy();
  stopSnake();
  stopTyping();
  stopCar();

  isGuest = false;
  $("pin-entry").value = "";
  $("pin-message").textContent = "";
  showPage("login-page");
}

function unlockApp() {
  const entered = $("pin-entry").value;

  if (entered === appPin) {
    $("pin-entry").value = "";
    $("pin-message").textContent = "";
    enterHome();
  } else {
    $("pin-message").textContent = "Incorrect PIN. Try again.";
  }
}

// CALCULATOR

function calcUpdate() {
  $("calc-display").textContent = calcExpression || "0";
}

function calcInput(value) {
  if (calcExpression.length > 35) return;

  if (calcExpression === "Error") calcExpression = "";

  calcExpression += value;
  calcUpdate();
}

function calcClear() {
  calcExpression = "";
  calcUpdate();
}

function calcBack() {
  calcExpression = calcExpression.slice(0, -1);
  calcUpdate();
}

function calcResult() {
  try {
    if (
      !calcExpression ||
      !/^[0-9+\-*/%.() ]+$/.test(calcExpression)
    ) throw Error();

    const result = Function(
      '"use strict";return (' + calcExpression + ')'
    )();

    if (!Number.isFinite(result)) throw Error();

    calcExpression = String(Number(result.toFixed(10)));
  } catch (e) {
    calcExpression = "Error";
  }

  calcUpdate();
}

// PASSWORD GENERATOR

function generatePassword() {
  let length = parseInt($("pass-length").value, 10);

  if (!Number.isFinite(length)) length = 16;
  length = Math.max(6, Math.min(40, length));

  $("pass-length").value = length;

  const chars =
    "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789!@#$%&*?";

  let result = "";
  const random = new Uint32Array(length);

  if (window.crypto && window.crypto.getRandomValues) {
    window.crypto.getRandomValues(random);
  } else {
    for (let i = 0; i < length; i++) {
      random[i] = Math.floor(Math.random() * 100000);
    }
  }

  for (let i = 0; i < length; i++) {
    result += chars[random[i] % chars.length];
  }

  $("password-output").textContent = result;
}

async function copyPassword() {
  const value = $("password-output").textContent;

  if (!value || value === "Your password appears here.") return;

  try {
    await navigator.clipboard.writeText(value);
    $("password-output").textContent = value + "  ✓ Copied";
  } catch (e) {
    $("password-output").textContent = value + "  (Select to copy)";
  }
}
// NOTES

function getNotes() {
  return store.get("mobile_notes", []);
}

function saveNote() {
  const title = $("note-title").value.trim();
  const body = $("note-body").value.trim();

  if (!title && !body) return;

  const notes = getNotes();

  notes.unshift({
    id: Date.now(),
    title: title || "Untitled",
    body
  });

  store.set("mobile_notes", notes);

  $("note-title").value = "";
  $("note-body").value = "";

  renderNotes();
}

function renderNotes() {
  const notes = getNotes();
  $("notes-list").innerHTML = "";

  if (!notes.length) {
    $("notes-list").innerHTML =
      '<p class="small-note">No notes yet. Create your first note.</p>';
    return;
  }

  notes.forEach(note => {
    const card = document.createElement("div");
    card.className = "card";
    card.style.marginBottom = "10px";

    const heading = document.createElement("h3");
    heading.textContent = note.title;

    const content = document.createElement("p");
    content.textContent = note.body;

    const remove = document.createElement("button");
    remove.className = "secondary";
    remove.textContent = "DELETE";

    remove.onclick = () => {
      store.set(
        "mobile_notes",
        getNotes().filter(n => n.id !== note.id)
      );
      renderNotes();
    };

    card.append(heading, content, remove);
    $("notes-list").appendChild(card);
  });
}

// SETTINGS

function saveSettings() {
  const name = $("setting-name").value.trim() || "Guest";
  const pin = $("setting-pin").value.trim();

  if (pin && !/^\d{4,8}$/.test(pin)) {
    alert("PIN must contain 4 to 8 digits.");
    return;
  }

  userName = name;
  appPin = pin;

  store.set("mobile_name", name);
  store.set("mobile_pin", pin);

  $("welcome-name").textContent = "Hello, " + userName + "!";

  alert("Settings saved successfully.");
  goHome();
}

// NUMBER GUESSING GAME

function resetGuess() {
  secretNumber = Math.floor(Math.random() * 100) + 1;
  guessCount = 0;
  guessFinished = false;

  $("guess-input").value = "";
  $("guess-message").textContent =
    "10 chances remaining. Guess from 1 to 100.";
}

function makeGuess() {
  if (guessFinished) return;

  const guess = Number($("guess-input").value);

  if (!Number.isInteger(guess) || guess < 1 || guess > 100) {
    $("guess-message").textContent =
      "Enter a number from 1 to 100.";
    return;
  }

  guessCount++;
  const remaining = 10 - guessCount;

  if (guess === secretNumber) {
    $("guess-message").textContent =
      "🎉 Correct! You guessed it in " + guessCount + " attempts.";
    guessFinished = true;
  } else if (guessCount >= 10) {
    $("guess-message").textContent =
      "Game over! The number was " + secretNumber + ".";
    guessFinished = true;
  } else {
    $("guess-message").textContent =
      (guess < secretNumber
        ? "Too low! Try higher."
        : "Too high! Try lower.") +
      " " + remaining + " chances left.";
  }

  $("guess-input").value = "";
}

// TYPING SPEED GAME

const typingParagraphs = [
  "Technology has changed the way people communicate, learn and work. Every day, new ideas and inventions make life more connected. Learning how to use these tools wisely can help us become more creative and productive.",
  "Success is not always about doing something quickly. It is about staying consistent, learning from mistakes and improving a little every day. Small efforts can create meaningful results over time.",
  "A peaceful morning can make the entire day feel better. Fresh air, a clear mind and a positive attitude help us focus on important tasks. Good habits often begin with simple daily actions.",
  "Reading is a powerful way to explore new ideas and understand the world. Books introduce us to different people, places and experiences. Even a few minutes of reading can improve knowledge and vocabulary.",
  "The world around us is full of interesting discoveries. Science helps us understand nature, space, energy and the human body. Asking questions and exploring answers is an important part of learning.",
  "Time is valuable, so it is important to use it carefully. Planning our tasks can reduce stress and help us achieve our goals. A balanced routine also leaves room for rest and enjoyment.",
  "Good communication is an important skill in everyday life. Listening carefully, choosing clear words and respecting other opinions can make conversations more meaningful. Practice helps people express ideas with confidence.",
  "Nature gives us beautiful landscapes, fresh air and many useful resources. Protecting the environment is a shared responsibility. Simple actions such as saving water and reducing waste can make a difference.",
  "Every challenge gives us a chance to learn something new. Instead of giving up when a task becomes difficult, we can try another approach. Patience and practice help us move forward.",
  "A healthy routine includes enough sleep, regular movement and balanced meals. These habits support concentration and energy throughout the day. Taking care of ourselves helps us enjoy everyday activities."
];

function getRandomTypingParagraph() {
  let available = typingParagraphs
    .map((p, i) => i)
    .filter(i => !typingUsed.includes(i));

  if (!available.length) {
    typingUsed = [];
    available = typingParagraphs.map((p, i) => i);
  }

  const selected =
    available[Math.floor(Math.random() * available.length)];

  typingUsed.push(selected);
  return typingParagraphs[selected];
}

function startTyping() {
  stopTyping();

  typingText = getRandomTypingParagraph();
  typingSeconds = 60;
  typingStarted = true;
  typingStartTime = Date.now();

  $("typing-sentence").textContent = typingText;
  $("typing-input").value = "";
  $("typing-input").disabled = false;
  $("typing-input").focus();

  $("typing-time").textContent = "60";
  $("typing-live-wpm").textContent = "0";
  $("typing-results").classList.add("hidden");
  $("typing-result").textContent = "";
  $("typing-start-button").textContent = "RESTART TEST";

  $("typing-input").oninput = updateTypingProgress;

  typingTimer = setInterval(() => {
    const elapsed = Math.floor(
      (Date.now() - typingStartTime) / 1000
    );

    typingSeconds = Math.max(0, 60 - elapsed);
    $("typing-time").textContent = typingSeconds;

    updateTypingStats();

    if (typingSeconds <= 0) finishTyping();
  }, 250);
}

function getTypingStats() {
  const typed = $("typing-input").value;
  let correct = 0;
  let mistakes = 0;

  for (let i = 0; i < typed.length; i++) {
    if (typed[i] === typingText[i]) correct++;
    else mistakes++;
  }

  const total = typed.length;
  const accuracy = total ? Math.round(correct / total * 100) : 0;
  const elapsed = Math.max(
    1,
    (Date.now() - typingStartTime) / 1000
  );

  const wpm = Math.round((correct / 5) / (elapsed / 60));

  return {typed, correct, mistakes, total, accuracy, wpm};
}

function updateTypingStats() {
  if (!typingStarted) return;

  const stats = getTypingStats();
  $("typing-live-wpm").textContent = stats.wpm;
}

function updateTypingProgress() {
  if (!typingStarted) return;

  const stats = getTypingStats();
  $("typing-live-wpm").textContent = stats.wpm;

  if (stats.typed === typingText) finishTyping();
}

function finishTyping() {
  if (!typingStarted) return;

  const stats = getTypingStats();
  stopTyping();

  $("typing-input").disabled = true;
  $("typing-time").textContent = "0";

  $("typing-final-wpm").textContent = stats.wpm;
  $("typing-accuracy").textContent = stats.accuracy + "%";
  $("typing-correct").textContent = stats.correct;
  $("typing-mistakes").textContent = stats.mistakes;

  $("typing-result").textContent =
    stats.typed === typingText
      ? "Paragraph completed! Excellent work."
      : "Time is up! Here is your result.";

  $("typing-results").classList.remove("hidden");
  $("typing-start-button").textContent = "START NEW TEST";
}

// FLAPPY BIRD
const fc = $("flappy-canvas");
const fx = fc.getContext("2d");

function drawFlappy() {
  const w=fc.width,h=fc.height;
  
  const sky=fx.createLinearGradient(0,0,0,h);
  
  sky.addColorStop(0,"#55b9ed");
  sky.addColorStop(.48,"#a9e3f2");
  sky.addColorStop(.78,"#e3f2dc");
  sky.addColorStop(1,"#f5e5b7");
  
  fx.fillStyle=sky;
  fx.fillRect(0,0,w,h);
  
  const glow=fx.createRadialGradient(w*.78,h*.17,2,w*.78,h*.17,90);
  
  glow.addColorStop(0,"rgba(255,246,190,.88)");
  glow.addColorStop(.25,"rgba(255,239,173,.36)");
  glow.addColorStop(1,"rgba(255,239,173,0)");
  
  fx.fillStyle=glow;
  fx.fillRect(0,0,w,h*.42);
  fx.fillStyle="rgba(255,248,215,.72)";
  fx.beginPath();
  fx.arc(w*.78,h*.17,19,0,Math.PI*2);
  fx.fill();
  
  function cloud(x,y,scale,alpha=1){fx.save();
  fx.translate(x,y);
  fx.scale(scale,scale);
  fx.globalAlpha=alpha;
  const g=fx.createLinearGradient(0,-18,0,15);
  g.addColorStop(0,"#fff");
  g.addColorStop(.7,"#f5fbff");
  g.addColorStop(1,"#c9e0e8");
  fx.fillStyle=g;
  fx.beginPath();
  fx.ellipse(0,2,28,12,0,0,Math.PI*2);
  fx.ellipse(-17,0,14,12,0,0,Math.PI*2);
  fx.ellipse(2,-9,17,15,0,0,Math.PI*2);
  fx.ellipse(20,0,16,11,0,0,Math.PI*2);
  fx.fill();
  fx.restore();
  }
  cloud(54,70,.9,.92);
  cloud(208,116,1.12,.72);
  cloud(310,49,.7,.76);
  
  fx.fillStyle="#9ac9b5";
  fx.beginPath();
  fx.moveTo(0,h-125);
  fx.lineTo(0,h-190);
  fx.quadraticCurveTo(48,h-244,103,h-177);
  fx.quadraticCurveTo(152,h-228,207,h-174);
  fx.quadraticCurveTo(267,h-230,w,h-164);
  fx.lineTo(w,h-95);
  fx.closePath();
  fx.fill();
  
  fx.fillStyle="#6fae83";
  fx.beginPath();
  fx.moveTo(0,h-103);
  fx.quadraticCurveTo(60,h-160,127,h-111);
  fx.quadraticCurveTo(220,h-174,w,h-112);
  fx.lineTo(w,h-35);
  fx.lineTo(0,h-35);
  fx.closePath();
  fx.fill();
  
  fx.fillStyle="#4d956c";
  fx.beginPath();
  fx.moveTo(0,h-72);
  fx.quadraticCurveTo(76,h-120,148,h-76);
  fx.quadraticCurveTo(238,h-130,w,h-70);
  fx.lineTo(w,h-35);
  fx.lineTo(0,h-35);
  fx.closePath();
  fx.fill();
  
  for(let i=0;
  i<22;
  i++){const tx=(i*53+17)%w,ty=h-104-(i%3)*10;
  fx.fillStyle=i%2?"#477e58":"#386f50";
  fx.beginPath();
  fx.moveTo(tx,ty+13);
  fx.lineTo(tx+5,ty-5-(i%4)*2);
  fx.lineTo(tx+10,ty+13);
  fx.closePath();
  fx.fill();
  }
  const groundY=h-35,turf=fx.createLinearGradient(0,groundY,0,h);
  turf.addColorStop(0,"#78bd63");
  turf.addColorStop(.2,"#4c9b55");
  turf.addColorStop(1,"#287344");
  fx.fillStyle=turf;
  fx.fillRect(0,groundY,w,35);
  fx.fillStyle="#a8d978";
  fx.fillRect(0,groundY,w,5);
  
  for(let gx=3;
  gx<w;
  gx+=13){const gh=4+(gx*7%8);
  fx.strokeStyle=gx%2?"#d0e88b":"#3e8548";
  fx.lineWidth=1.4;
  fx.beginPath();
  fx.moveTo(gx,h-2);
  fx.lineTo(gx-2,h-gh);
  fx.moveTo(gx+3,h-2);
  fx.lineTo(gx+5,h-gh+2);
  fx.stroke();
  }
  if(flappyBird){
    fx.save();
  fx.translate(flappyBird.x,flappyBird.y);
  fx.rotate(Math.max(-.42,Math.min(.68,flappyBird.velocity*.045)));
  const beat=Math.sin(Date.now()/72);
    const body=fx.createRadialGradient(-4,-8,2,0,1,22);
  body.addColorStop(0,"#fff18a");
  body.addColorStop(.48,"#ffd84f");
  body.addColorStop(1,"#e99a25");
  fx.fillStyle=body;
  fx.beginPath();
  fx.ellipse(0,0,17,13,0,0,Math.PI*2);
  fx.fill();
  
    const chest=fx.createRadialGradient(8,4,1,8,5,12);
  chest.addColorStop(0,"#fff0a2");
  chest.addColorStop(1,"#f4bd3c");
  fx.fillStyle=chest;
  fx.beginPath();
  fx.ellipse(8,4,8,8,.25,0,Math.PI*2);
  fx.fill();
  
    fx.save();
  fx.translate(-4,1);
  fx.rotate(beat*.24);
  const wing=fx.createLinearGradient(-13,-12,8,11);
  wing.addColorStop(0,"#ffe98a");
  wing.addColorStop(.55,"#f5b832");
  wing.addColorStop(1,"#d98222");
  fx.fillStyle=wing;
  fx.beginPath();
  fx.moveTo(8,-2);
  fx.quadraticCurveTo(-1,-17,-17,-13);
  fx.quadraticCurveTo(-13,-5,-18,1);
  fx.quadraticCurveTo(-11,10,5,8);
  fx.quadraticCurveTo(10,4,8,-2);
  fx.closePath();
  fx.fill();
  fx.strokeStyle="#c77e22";
  fx.lineWidth=1.1;
  for(let f=0;
  f<4;
  f++){fx.beginPath();
  fx.moveTo(-11+f*3,-8+f*2);
  fx.quadraticCurveTo(-7+f*3,-2+f*2,-12+f*3,4+f);
  fx.stroke();
  }fx.restore();
  
    fx.fillStyle="#e9a12c";
  fx.beginPath();
  fx.moveTo(-3,-11);
  fx.quadraticCurveTo(-10,-19,-12,-17);
  fx.quadraticCurveTo(-11,-10,-5,-8);
  fx.closePath();
  fx.fill();
  
    fx.fillStyle="#fff";
  fx.beginPath();
  fx.arc(8,-6,5.4,0,Math.PI*2);
  fx.fill();
  fx.fillStyle="#26313a";
  fx.beginPath();
  fx.arc(10,-6,2.7,0,Math.PI*2);
  fx.fill();
  fx.fillStyle="#fff";
  fx.beginPath();
  fx.arc(10.8,-7,1,0,Math.PI*2);
  fx.fill();
  
    fx.strokeStyle="#8e5a1e";
  fx.lineWidth=1.2;
  fx.beginPath();
  fx.moveTo(4,-12);
  fx.quadraticCurveTo(8,-15,12,-12);
  fx.stroke();
  
    fx.fillStyle="#f18a2c";
  fx.beginPath();
  fx.moveTo(14,-2);
  fx.lineTo(27,1);
  fx.lineTo(15,6);
  fx.quadraticCurveTo(13,3,14,-2);
  fx.closePath();
  fx.fill();
  fx.fillStyle="#ffc05a";
  fx.beginPath();
  fx.moveTo(15,-2);
  fx.lineTo(25,1);
  fx.lineTo(15,2);
  fx.closePath();
  fx.fill();
  
    fx.strokeStyle="#d97827";
  fx.lineWidth=1.5;
  [-5,5].forEach(px=>{fx.beginPath();
  fx.moveTo(px,10);
  fx.lineTo(px-1,15);
  fx.lineTo(px-5,16);
  fx.moveTo(px-1,15);
  fx.lineTo(px+3,17);
  fx.stroke();
  });
  
    fx.strokeStyle="rgba(255,255,220,.7)";
  fx.lineWidth=.8;
  fx.beginPath();
  fx.moveTo(-7,-5);
  fx.quadraticCurveTo(-1,-9,4,-5);
  fx.stroke();
  fx.restore();
  
  }
  flappyPipes.forEach(p=>{const grad=fx.createLinearGradient(p.x,0,p.x+48,0);
  grad.addColorStop(0,"#164e3e");
  grad.addColorStop(.16,"#2d8a55");
  grad.addColorStop(.42,"#8bcf70");
  grad.addColorStop(.7,"#348451");
  grad.addColorStop(1,"#123c34");
  const body=(x,y,ww,hh)=>{if(hh<=0)return;
  fx.fillStyle=grad;
  fx.fillRect(x,y,ww,hh);
  fx.fillStyle="rgba(235,255,208,.2)";
  fx.fillRect(x+7,y+2,4,Math.max(0,hh-4));
  fx.fillStyle="rgba(0,20,18,.22)";
  fx.fillRect(x+ww-7,y+2,4,Math.max(0,hh-4));
  fx.strokeStyle="#123c2d";
  fx.lineWidth=3;
  fx.strokeRect(x+1.5,y+1.5,ww-3,Math.max(0,hh-3));
  };
  const cap=(x,y,ww,hh)=>{const g=fx.createLinearGradient(x,y,x+ww,y);
  g.addColorStop(0,"#164b38");
  g.addColorStop(.2,"#3c9c5e");
  g.addColorStop(.5,"#a0d77c");
  g.addColorStop(.82,"#38824d");
  g.addColorStop(1,"#123c31");
  fx.fillStyle=g;
  fx.fillRect(x,y,ww,hh);
  fx.strokeStyle="#123c2d";
  fx.lineWidth=3;
  fx.strokeRect(x+1.5,y+1.5,ww-3,hh-3);
  };
  body(p.x,0,48,p.top-12);
  cap(p.x-4,p.top-13,56,14);
  body(p.x,p.bottom+12,48,h-p.bottom-47);
  cap(p.x-4,p.bottom,56,14);
  });
  
  if(!flappyRunning){fx.fillStyle="rgba(13,48,61,.64)";
  fx.beginPath();
  fx.roundRect(w/2-105,h/2-23,210,46,13);
  fx.fill();
  fx.fillStyle="#fff";
  fx.textAlign="center";
  fx.font="bold 17px Arial";
  fx.fillText("Tap PLAY to start",w/2,h/2+6);
  }
}
function startFlappy() {
  stopFlappy();

  flappyBird = {x:80, y:200, velocity:0};
  flappyPipes = [];
  flappyScore = 0;

  $("flappy-score").textContent = "Score: 0";
  flappyRunning = true;

  let frame = 0;

  flappyTimer = setInterval(() => {
    if (!flappyRunning) return;

    frame++;

    flappyBird.velocity += 0.45;
    flappyBird.y += flappyBird.velocity;

    if (frame % 68 === 0) {
      const top = 55 + Math.random() * 135;

      flappyPipes.push({
        x:fc.width,
        top,
        bottom:top + 82,
        passed:false
      });
    }

    flappyPipes.forEach(p => {
      p.x -= 4.2;

      if (!p.passed && p.x + 48 < flappyBird.x) {
        p.passed = true;
        flappyScore++;
        mobileSfx("point");
        $("flappy-score").textContent = "Score: " + flappyScore;
      }

      const overlaps =
        flappyBird.x + 11 > p.x &&
        flappyBird.x - 11 < p.x + 48;

      const hitsPipe =
        flappyBird.y - 11 < p.top ||
        flappyBird.y + 11 > p.bottom;

      if (overlaps && hitsPipe) endFlappy();
    });

    flappyPipes = flappyPipes.filter(p => p.x > -55);

    if (
      flappyBird.y > fc.height - 48 ||
      flappyBird.y < 10
    ) endFlappy();

    drawFlappy();
  }, 25);
}

function flap() {
  if (!flappyRunning) return;
  flappyBird.velocity = -6.8;
}

function endFlappy() {
  if (!flappyRunning) return;

  stopFlappy();
  drawFlappy();

  $("flappy-score").textContent =
    "Game over! Score: " + flappyScore;
}

fc.addEventListener("pointerdown", flap);

// SNAKE

const sc = $("snake-canvas");
const sx = sc.getContext("2d");
const cell = 20;
const gridSize = 14;

function newSnakeFood() {
  let point;

  do {
    point = {
      x:Math.floor(Math.random() * gridSize),
      y:Math.floor(Math.random() * gridSize)
    };
  } while (
    snakeBody.some(p => p.x === point.x && p.y === point.y)
  );

  return point;
}

function resetSnake() {
  stopSnake();

  snakeBody = [
    {x:5,y:7},
    {x:4,y:7},
    {x:3,y:7}
  ];
  snakePreviousBody = snakeBody.map(p => ({...p}));

  snakeDir = {x:1,y:0};
  snakeNextDir = {x:1,y:0};
  snakeFood = newSnakeFood();
  snakePoints = 0;
  snakeStep = 125;
  snakeAccumulator = 0;
  snakeLastTime = 0;

  $("snake-score").textContent = "Score: 0";
  drawSnake();
}

function drawSnake() {
  const w = sc.width;
  const h = sc.height;

  // Calm, layered green garden background.
  const bg = sx.createLinearGradient(0, 0, w, h);
  bg.addColorStop(0, "#174b3b");
  bg.addColorStop(0.52, "#0d684d");
  bg.addColorStop(1, "#123b50");
  sx.fillStyle = bg;
  sx.fillRect(0, 0, w, h);

  // Subtle leafy shapes add texture without a distracting dotted grid.
  sx.save();
  sx.globalAlpha = 0.12;
  for (let i = 0; i < 14; i++) {
    const x = (i * 47 + 19) % w;
    const y = (i * 71 + 13) % h;
    sx.fillStyle = i % 2 ? "#c4ffcf" : "#69e6b0";
    sx.beginPath();
    sx.ellipse(x, y, 18, 6, -0.6, 0, Math.PI * 2);
    sx.fill();
  }
  sx.restore();

  // Interpolate between grid steps so the snake glides instead of jumping.
  const progress = snakeRunning ? Math.min(1, snakeAccumulator / snakeStep) : 1;
  const points = snakeBody.map((p, i) => {
    const old = snakePreviousBody[i] || p;
    return {
      x: (old.x + (p.x - old.x) * progress) * cell + cell / 2,
      y: (old.y + (p.y - old.y) * progress) * cell + cell / 2
    };
  });

  // Small, clearly visible apple.
  if (snakeFood) {
    const fx = snakeFood.x * cell + cell / 2;
    const fy = snakeFood.y * cell + cell / 2;
    sx.save();
    sx.shadowColor = "#ff4355";
    sx.shadowBlur = 8;
    sx.fillStyle = "#ff4055";
    sx.beginPath();
    sx.arc(fx - 3, fy + 1, 5, 0, Math.PI * 2);
    sx.arc(fx + 3, fy + 1, 5, 0, Math.PI * 2);
    sx.fill();
    sx.shadowBlur = 0;
    sx.strokeStyle = "#74452a";
    sx.lineWidth = 1.5;
    sx.beginPath();
    sx.moveTo(fx, fy - 3);
    sx.lineTo(fx + 1, fy - 8);
    sx.stroke();
    sx.fillStyle = "#9cff9c";
    sx.beginPath();
    sx.ellipse(fx + 4, fy - 6, 3, 1.7, -0.5, 0, Math.PI * 2);
    sx.fill();
    sx.restore();
  }

  // Continuous rounded snake body, not separate dotted blocks.
  if (points.length > 1) {
    sx.save();
    sx.lineCap = "round";
    sx.lineJoin = "round";
    sx.strokeStyle = "#2f8e48";
    sx.lineWidth = 15;
    sx.beginPath();
    points.forEach((point, i) => {
      if (i === 0) sx.moveTo(point.x, point.y);
      else sx.lineTo(point.x, point.y);
    });
    sx.stroke();
    sx.strokeStyle = "#a9e65d";
    sx.lineWidth = 9;
    sx.stroke();
    sx.strokeStyle = "rgba(28,101,49,.62)";
    sx.lineWidth = 1;
    for(let i=1;i<points.length;i++){
      const p=points[i];sx.beginPath();sx.arc(p.x,p.y,5.2,.25,Math.PI-.25);sx.stroke();
    }
    sx.restore();
  }

  // Distinct head, eyes and a small mouth.
  if (points.length) {
    const head = points[0];
    sx.save();
    sx.translate(head.x, head.y);
    const angle = Math.atan2(snakeDir.y, snakeDir.x);
    sx.rotate(angle);
    const headPaint=sx.createLinearGradient(-3,-9,8,9);headPaint.addColorStop(0,"#e7f6a0");headPaint.addColorStop(.48,"#a9dc55");headPaint.addColorStop(1,"#4c9d43");
    sx.fillStyle=headPaint;sx.beginPath();sx.moveTo(-9,-7);sx.quadraticCurveTo(-2,-11,5,-7);sx.quadraticCurveTo(12,-5,13,0);sx.quadraticCurveTo(12,5,5,7);sx.quadraticCurveTo(-2,11,-9,7);sx.quadraticCurveTo(-13,0,-9,-7);sx.closePath();sx.fill();sx.strokeStyle="#d9f7a0";sx.lineWidth=1.1;sx.stroke();
    [-1,1].forEach(side=>{sx.fillStyle="#f7ffd7";sx.beginPath();sx.ellipse(4,side*4.7,3.2,2.7,0,0,Math.PI*2);sx.fill();sx.fillStyle="#172b1c";sx.beginPath();sx.ellipse(5.1,side*4.7,1.15,2.05,0,0,Math.PI*2);sx.fill();sx.fillStyle="#fff";sx.beginPath();sx.arc(5.5,side*4.1,.65,0,Math.PI*2);sx.fill();});
    sx.fillStyle="#315d2b";sx.beginPath();sx.arc(11,-2.2,.85,0,Math.PI*2);sx.arc(11,2.2,.85,0,Math.PI*2);sx.fill();
    sx.strokeStyle="#315d2b";sx.lineWidth=1;sx.beginPath();sx.moveTo(5,0);sx.quadraticCurveTo(9,1,12,0);sx.stroke();
    sx.strokeStyle="#ed6573";sx.lineWidth=1.5;sx.lineCap="round";sx.beginPath();sx.moveTo(12,0);sx.lineTo(17,0);sx.lineTo(20,-2.5);sx.moveTo(17,0);sx.lineTo(20,2.5);sx.stroke();
    sx.strokeStyle="rgba(242,255,190,.65)";sx.lineWidth=.7;sx.beginPath();sx.arc(-2,-2,3.1,.1,2.5);sx.arc(-2,2,3.1,-2.5,-.1);sx.stroke();
    sx.restore();
  }

  if (!snakeRunning) {
    sx.fillStyle = "#fff";
    sx.textAlign = "center";
    sx.font = "bold 16px Arial";
    sx.fillText("Press PLAY to start", w / 2, h / 2);
  }
}
function snakeMove() {
  snakePreviousBody = snakeBody.map(p => ({...p}));
  snakeDir = {...snakeNextDir};

  const head = {
    x:snakeBody[0].x + snakeDir.x,
    y:snakeBody[0].y + snakeDir.y
  };

  const eating =
    head.x === snakeFood.x &&
    head.y === snakeFood.y;

  const bodyToCheck = eating
    ? snakeBody
    : snakeBody.slice(0, -1);

  if (
    head.x < 0 || head.y < 0 ||
    head.x >= gridSize || head.y >= gridSize ||
    bodyToCheck.some(p => p.x === head.x && p.y === head.y)
  ) {
    stopSnake();
    $("snake-score").textContent =
      "Game over! Score: " + snakePoints;
    drawSnake();
    return;
  }

  snakeBody.unshift(head);

  if (eating) {
    snakePoints++;
    snakeFood = newSnakeFood();

    $("snake-score").textContent = "Score: " + snakePoints;
    snakeStep = Math.max(112, 125 - snakePoints * 0.35);
  } else {
    snakeBody.pop();
  }

  drawSnake();
}

function snakeAnimation(timestamp) {
  if (!snakeRunning) return;

  if (!snakeLastTime) snakeLastTime = timestamp;

  const delta = Math.min(timestamp - snakeLastTime, 50);
  snakeLastTime = timestamp;
  snakeAccumulator += delta;

  while (snakeAccumulator >= snakeStep && snakeRunning) {
    snakeAccumulator -= snakeStep;
    snakeMove();
  }

  if (snakeRunning) {
    snakeFrame = requestAnimationFrame(snakeAnimation);
  }
}

function startSnake() {
  resetSnake();

  snakeRunning = true;
  drawSnake();

  snakeFrame = requestAnimationFrame(snakeAnimation);
}

function snakeDirection(x, y) {
  if (!snakeRunning) return;

  if (x === -snakeDir.x && y === -snakeDir.y) return;

  snakeNextDir = {x,y};
}

sc.addEventListener("touchstart", e => {
  const t = e.touches[0];
  snakeTouchStart = {x:t.clientX,y:t.clientY};
}, {passive:true});

sc.addEventListener("touchmove", e => {
  if (snakeTouchStart) e.preventDefault();
}, {passive:false});

sc.addEventListener("touchend", e => {
  if (!snakeTouchStart) return;

  const t = e.changedTouches[0];
  const dx = t.clientX - snakeTouchStart.x;
  const dy = t.clientY - snakeTouchStart.y;

  if (Math.max(Math.abs(dx), Math.abs(dy)) > 20) {
    if (Math.abs(dx) > Math.abs(dy)) {
      snakeDirection(dx > 0 ? 1 : -1, 0);
    } else {
      snakeDirection(0, dy > 0 ? 1 : -1);
    }
  }

  snakeTouchStart = null;
}, {passive:true});

// CAR RACING GAME

const cc = $("car-canvas");
const cx = cc.getContext("2d");

const carRoad = {
  left:35,
  right:305,
  width:270,
  laneWidth:90
};

function carLaneX(lane) {
  return carRoad.left + carRoad.laneWidth * lane +
    carRoad.laneWidth / 2;
}

// Keep the player's car centered on the road before the game starts.
carPlayerX = carLaneX(1);

function carPath(ctx, points, close=true) {
  ctx.beginPath();
  points.forEach((p,i)=>i?ctx.lineTo(p[0],p[1]):ctx.moveTo(p[0],p[1]));
  if(close)ctx.closePath();
}

function drawCarVehicle(ctx, x, y, color, scale=1, type='sport', player=false) {
  ctx.save();
  ctx.translate(x,y);
  // Straight front-facing vehicle: no rotation or perspective shear.
  ctx.scale(scale,scale);
  const bodyW = type==='van'?31:type==='suv'?29:type==='truck'?33:25;
  const bodyH = type==='van'?61:type==='truck'?66:type==='suv'?58:53;
  // soft ground shadow
  ctx.fillStyle='rgba(0,0,0,.38)';ctx.beginPath();ctx.ellipse(1,5,bodyW*.92,bodyH*.55,0,0,Math.PI*2);ctx.fill();
  // wheels and wheel arches
  ctx.fillStyle='#10151c';
  [-1,1].forEach(side=>[-.62,.58].forEach(pos=>{
    ctx.beginPath();ctx.roundRect(side*(bodyW*.43)-3,pos*bodyH*.34-8,7,17,3);ctx.fill();
    ctx.fillStyle='#697783';ctx.fillRect(side*(bodyW*.43)-1,pos*bodyH*.34-5,3,10);ctx.fillStyle='#10151c';
  }));
  // main body with a tapered bonnet and rounded shoulders
  const paint=ctx.createLinearGradient(-bodyW,0,bodyW,0);
  paint.addColorStop(0,'#26313c');paint.addColorStop(.16,color);paint.addColorStop(.48,'#ffffff55');paint.addColorStop(.72,color);paint.addColorStop(1,'#111a25');
  ctx.fillStyle=paint;
  ctx.beginPath();
  ctx.moveTo(-bodyW*.28,-bodyH*.5);ctx.quadraticCurveTo(-bodyW*.48,-bodyH*.5,-bodyW*.48,-bodyH*.34);
  ctx.lineTo(-bodyW*.5,bodyH*.31);ctx.quadraticCurveTo(-bodyW*.48,bodyH*.5,-bodyW*.25,bodyH*.5);
  ctx.lineTo(bodyW*.25,bodyH*.5);ctx.quadraticCurveTo(bodyW*.48,bodyH*.5,bodyW*.5,bodyH*.31);
  ctx.lineTo(bodyW*.48,-bodyH*.34);ctx.quadraticCurveTo(bodyW*.48,-bodyH*.5,bodyW*.28,-bodyH*.5);ctx.closePath();ctx.fill();
  ctx.strokeStyle='#ffffff88';ctx.lineWidth=1.2;ctx.stroke();
  const bonnet=ctx.createLinearGradient(0,-bodyH*.5,0,-bodyH*.18);
  bonnet.addColorStop(0,'#ffffff55');bonnet.addColorStop(1,'#ffffff00');
  ctx.fillStyle=bonnet;ctx.beginPath();ctx.moveTo(-bodyW*.27,-bodyH*.47);ctx.lineTo(bodyW*.27,-bodyH*.47);ctx.lineTo(bodyW*.23,-bodyH*.20);ctx.lineTo(-bodyW*.23,-bodyH*.20);ctx.closePath();ctx.fill();
  // cabin and panoramic glass
  const cabinTop=type==='van'?-bodyH*.35:-bodyH*.29;
  const cabinBottom=type==='truck'?bodyH*.12:bodyH*.17;
  ctx.fillStyle='#172d3b';
  ctx.beginPath();ctx.moveTo(-bodyW*.34,cabinBottom);ctx.lineTo(-bodyW*.27,cabinTop+7);ctx.quadraticCurveTo(0,cabinTop-5,bodyW*.27,cabinTop+7);ctx.lineTo(bodyW*.34,cabinBottom);ctx.closePath();ctx.fill();
  const glass=ctx.createLinearGradient(-bodyW*.2,cabinTop,bodyW*.2,cabinBottom);
  glass.addColorStop(0,'#b8f3ff');glass.addColorStop(.5,'#548ba5');glass.addColorStop(1,'#1a4058');
  ctx.fillStyle=glass;ctx.beginPath();ctx.moveTo(-bodyW*.27,cabinBottom-2);ctx.lineTo(-bodyW*.21,cabinTop+8);ctx.quadraticCurveTo(0,cabinTop+2,bodyW*.21,cabinTop+8);ctx.lineTo(bodyW*.27,cabinBottom-2);ctx.closePath();ctx.fill();
  ctx.strokeStyle='#d9f7ff99';ctx.lineWidth=1;ctx.stroke();
  // central roof / rear glass split
  ctx.strokeStyle='#d5f4ff66';ctx.beginPath();ctx.moveTo(0,cabinTop+5);ctx.lineTo(0,cabinBottom-1);ctx.stroke();
  // mirrors, headlights and tail lamps
  ctx.fillStyle=color;ctx.fillRect(-bodyW*.59,-bodyH*.19,5,9);ctx.fillRect(bodyW*.45,-bodyH*.19,5,9);
  ctx.fillStyle=player?'#fff8c6':'#fff3b1';ctx.shadowColor='#fff3b1';ctx.shadowBlur=player?13:7;
  ctx.beginPath();ctx.ellipse(-bodyW*.31,-bodyH*.43,4,3,0,0,Math.PI*2);ctx.ellipse(bodyW*.31,-bodyH*.43,4,3,0,0,Math.PI*2);ctx.fill();ctx.shadowBlur=0;
  ctx.fillStyle='#ff354f';ctx.fillRect(-bodyW*.36,bodyH*.42,6,4);ctx.fillRect(bodyW*.22,bodyH*.42,6,4);
  // bonnet creases, grille and sporty trim
  ctx.strokeStyle='#ffffff66';ctx.lineWidth=1.1;ctx.beginPath();ctx.moveTo(-bodyW*.22,-bodyH*.24);ctx.lineTo(-bodyW*.17,-bodyH*.4);ctx.moveTo(bodyW*.22,-bodyH*.24);ctx.lineTo(bodyW*.17,-bodyH*.4);ctx.stroke();
  ctx.fillStyle='#101a22';ctx.beginPath();ctx.roundRect(-bodyW*.22,-bodyH*.48,bodyW*.44,3,2);ctx.fill();
  if(player){
    ctx.fillStyle='#d9f8ff';ctx.fillRect(-bodyW*.23,bodyH*.48,bodyW*.46,3);
    ctx.fillStyle='#f7faff';ctx.shadowColor='#8eeaff';ctx.shadowBlur=15;ctx.fillRect(-bodyW*.31,-bodyH*.47,5,2);ctx.fillRect(bodyW*.2,-bodyH*.47,5,2);ctx.shadowBlur=0;
    ctx.fillStyle='#0e1b28';ctx.fillRect(-bodyW*.42,-bodyH*.55,bodyW*.84,4);
  }
  ctx.restore();
}

function drawCarRoadside(ctx,w,h,offset){
  // Soft, low-contrast roadside greenery: the road and cars stay the focus.
  const cycle=132;
  ctx.save();
  ctx.globalAlpha=.58;
  for(let y=-cycle;y<h+cycle;y+=cycle){
    const yy=((y+(offset*.62)%cycle)+cycle*2)%(h+cycle)-cycle;
    [-1,1].forEach(side=>{
      const x=side<0?13:327;
      ctx.fillStyle='#6e9c79';
      ctx.beginPath();ctx.ellipse(x,yy+24,17,11,0,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#91b58b';
      ctx.beginPath();ctx.arc(x-7,yy+19,8,0,Math.PI*2);ctx.arc(x+4,yy+15,10,0,Math.PI*2);ctx.arc(x+10,yy+25,7,0,Math.PI*2);ctx.fill();
      ctx.fillStyle='#c3d2a3';
      ctx.beginPath();ctx.arc(x-4,yy+13,2,0,Math.PI*2);ctx.arc(x+6,yy+18,1.7,0,Math.PI*2);ctx.fill();
      // Small pale roadside marker, without heavy lamps or dark poles.
      ctx.fillStyle='#e6e4c9';ctx.fillRect(side<0?28:307,yy+43,3,15);
      ctx.fillStyle='#e5bd72';ctx.fillRect(side<0?28:307,yy+45,3,4);
    });
  }
  ctx.restore();
}

function drawCar() {
  const w=cc.width,h=cc.height;
  const sky=cx.createLinearGradient(0,0,0,h);
  sky.addColorStop(0,'#9dc9d0');sky.addColorStop(.2,'#477b68');sky.addColorStop(.42,'#245b42');sky.addColorStop(1,'#183d30');
  cx.fillStyle=sky;cx.fillRect(0,0,w,h);
  // distant hills and roadside texture
  cx.fillStyle='#285642';cx.beginPath();cx.moveTo(0,115);cx.quadraticCurveTo(65,64,130,116);cx.quadraticCurveTo(235,55,340,112);cx.lineTo(340,190);cx.lineTo(0,190);cx.closePath();cx.fill();
  for(let i=0;i<24;i++){
    const x=(i*53+17)%340,y=105+(i%4)*18;
    cx.fillStyle=i%2?'#397a4a':'#1e593d';cx.beginPath();cx.arc(x,y,9+(i%3)*3,0,Math.PI*2);cx.fill();
  }
  // asphalt road and shoulder perspective
  cx.fillStyle='#c9c3aa';carPath(cx,[[25,0],[315,0],[340,h],[0,h]]);cx.fill();
  const roadGrad=cx.createLinearGradient(0,0,0,h);roadGrad.addColorStop(0,'#777f85');roadGrad.addColorStop(.55,'#646d75');roadGrad.addColorStop(1,'#515b64');
  cx.fillStyle=roadGrad;carPath(cx,[[48,0],[292,0],[310,h],[30,h]]);cx.fill();
  // rumble strips and reflective road edges
  for(let y=-50;y<h+70;y+=52){const yy=y+(carRoadOffset%52);cx.fillStyle='#f2e8c8';cx.fillRect(32,yy,4,22);cx.fillRect(304,yy,4,22);cx.fillStyle='#d9857b';cx.fillRect(32,yy+22,4,12);cx.fillRect(304,yy+22,4,12);}
  // lane dividers with moving dashes
  cx.fillStyle='#f4efcf';for(let lane=1;lane<=2;lane++){const x=carRoad.left+lane*carRoad.laneWidth-2;for(let y=-65;y<h+70;y+=88){cx.fillRect(x,y+(carRoadOffset%88),4,43);}}
  // subtle asphalt grain / tire-darkened strips
  cx.fillStyle='#ffffff09';for(let i=0;i<16;i++){const y=(i*43+carRoadOffset*.28)%(h+20)-10;cx.fillRect(55,y,2,13);cx.fillRect(283,y,2,13);}
  // roadside foliage, lamps and reflective markers stay visible above the shoulder.
  drawCarRoadside(cx,w,h,carRoadOffset);
  // distant vehicles are smaller; they grow as they approach the player
  carObstacles.slice().sort((a,b)=>a.y-b.y).forEach(obstacle=>{
    // Keep every traffic car the same size to avoid a zooming/pulsing effect.
    drawCarVehicle(cx,obstacle.x,obstacle.y,obstacle.color,1,obstacle.type||'sedan',false);
  });
  drawCarVehicle(cx,carPlayerX,h*.72,'#16a8e2',1,'sport',true);
  if(!carRunning){
    cx.fillStyle='rgba(7,19,30,.65)';cx.beginPath();cx.roundRect(45,218,250,68,15);cx.fill();
    cx.fillStyle='#fff';cx.textAlign='center';cx.font='900 19px Arial';cx.fillText('TAP PLAY TO START',w/2,246);
    cx.font='bold 10px Arial';cx.fillStyle='#d7efff';cx.fillText('DODGE TRAFFIC  •  STAY ON THE ROAD',w/2,266);
  }
}

function updateCarScore() {
  $("car-score").textContent = Math.floor(carScore);
  $("car-level").textContent =
    Math.floor(carScore / 10) + 1;

  $("car-speed").textContent =
    Math.min(10, carSpeed / 155).toFixed(1) + "x";
}

function moveCar(direction) {
  if (!carRunning) return;

  carPlayerLane = Math.max(
    0,
    Math.min(2, carPlayerLane + direction)
  );

  carPlayerX = carLaneX(carPlayerLane);
  drawCar();
}

function startCarGame() {
  stopCar();

  carRunning = true;
  carPlayerLane = 1;
  carPlayerX = carLaneX(1);
  carObstacles = [];
  carScore = 0;
  carSpeed = 232;
  carSpawnTimer = 0;
  carRoadOffset = 0;
  carLastTime = 0;

  $("car-message").textContent =
    "Use swipe, arrow keys or A/D to drive.";

  updateCarScore();
  drawCar();

  carFrame = requestAnimationFrame(carAnimation);
}

function carAnimation(timestamp) {
  if (!carRunning) return;

  if (!carLastTime) carLastTime = timestamp;

  const delta = Math.min((timestamp - carLastTime) / 1000, 0.05);
  carLastTime = timestamp;

  carScore += delta * 2;
  // Escalating challenge: starts fast and climbs smoothly to a hard 10x cap.
  carSpeed = Math.min(1550, 232 + carScore * 20);
  carRoadOffset += carSpeed * delta;

  carSpawnTimer += delta;

  if (carSpawnTimer >= Math.max(0.24, 0.72 - carScore * 0.0065)) {
    carSpawnTimer = 0;

    const lane = Math.floor(Math.random() * 3);

    carObstacles.push({
      lane,
      x:carLaneX(lane),
      y:-62,
      color:["#ff765f","#ffd166","#b28cff","#f1f4f5","#36c5a5","#e06b9b","#7c9cff"][Math.floor(Math.random()*7)],
      type:["sedan","suv","sport","van","truck"][Math.floor(Math.random()*5)]
    });
  }

  carObstacles.forEach(obstacle => {
    obstacle.y += carSpeed * delta;

    const closeX = Math.abs(obstacle.x - carPlayerX) < 31;
    const closeY = Math.abs(obstacle.y - cc.height*.72) < 42;

    if (closeX && closeY) {
      endCarGame();
    }
  });

  carObstacles = carObstacles.filter(
    obstacle => obstacle.y < cc.height + 60
  );

  updateCarScore();
  drawCar();

  if (carRunning) {
    carFrame = requestAnimationFrame(carAnimation);
  }
}

function endCarGame() {
  if (!carRunning) return;

  stopCar();

  $("car-message").textContent =
    "Game over! Final score: " + Math.floor(carScore) +
    ". Press PLAY to try again.";

  drawCar();
}

cc.addEventListener("pointerdown", e => {
  carTouchStart = {x:e.clientX,y:e.clientY};
}, {passive:true});

cc.addEventListener("pointerup", e => {
  if (!carTouchStart) return;

  const dx = e.clientX - carTouchStart.x;
  const dy = e.clientY - carTouchStart.y;

  if (!carRunning) {
    if (Math.max(Math.abs(dx), Math.abs(dy)) <= 20) {
      startCarGame();
    }
  } else if (Math.abs(dx) > 20) {
    moveCar(dx > 0 ? 1 : -1);
  }

  carTouchStart = null;
});

cc.addEventListener("pointercancel", () => {
  carTouchStart = null;
});

document.addEventListener("keydown", e => {
  if (!$("car-page") || $("car-page").classList.contains("hidden")) {
    return;
  }

  if (
    e.key === "ArrowLeft" ||
    e.key === "a" ||
    e.key === "A"
  ) {
    e.preventDefault();
    moveCar(-1);
  }

  if (
    e.key === "ArrowRight" ||
    e.key === "d" ||
    e.key === "D"
  ) {
    e.preventDefault();
    moveCar(1);
  }
});


// ================= NEON BREAKOUT: COMPLETE GAME SYSTEM =================
// ================= NEON BREAKOUT GAME =================
const nbCanvas=document.getElementById('nb-canvas');
const nbCtx=nbCanvas?nbCanvas.getContext('2d'):null;
const NB_W=360,NB_H=520,NB_LEVELS=30;
const nbColors=['#4de9e9','#8d78ff','#ff69b4','#ffb45d','#83f28f'];
let nbSave=nbLoad(),nbRunning=false,nbPaused=false,nbFrame=0,nbLast=0,nbPaddle={x:150,w:60},nbBalls=[],nbBricks=[],nbDrops=[],nbLasers=[],nbScore=0,nbLives=3,nbLevel=1,nbCoins=nbSave.coins,nbMove=0,nbEffects={wide:0,slow:0,laser:0},nbPointer=null,nbMessage='Tap START to play',nbLevelWon=false;
function nbLoad(){try{const d=JSON.parse(localStorage.getItem('mobile_neon_breakout_v1')||'{}');return {best:Number(d.best)||0,unlocked:Math.max(1,Math.min(30,Number(d.unlocked)||1)),cleared:Array.isArray(d.cleared)?d.cleared:[],coins:Number(d.coins)||0};}catch(e){return {best:0,unlocked:1,cleared:[],coins:0};}}
function nbPersist(){try{localStorage.setItem('mobile_neon_breakout_v1',JSON.stringify(nbSave));}catch(e){}nbRenderMeta();}
function nbRenderMeta(){const el=id=>document.getElementById(id);if(!el('nb-best'))return;el('nb-best').textContent=nbSave.best;el('nb-coins').textContent=nbSave.coins+' ✦';el('nb-progress-label').textContent=nbSave.cleared.length+' / 30 stages cleared';el('nb-progress').style.width=(nbSave.cleared.length/30*100)+'%';el('nb-levels').innerHTML=Array.from({length:30},(_,i)=>'<button class="nb-level '+(i+1===nbLevel?'current':'')+'" '+(i+1>nbSave.unlocked?'disabled':'')+' onclick="breakoutSetLevel('+(i+1)+')">'+String(i+1).padStart(2,'0')+'</button>').join('');}
function nbResetStage(){nbPaddle={x:150,w:nbEffects.wide>0?92:60};nbBalls=[{x:180,y:455,vx:2.3,vy:-3.5,r:6,stuck:true}];nbDrops=[];nbLasers=[];nbLevelWon=false;nbBricks=[];const
rows=3+Math.min(4,Math.floor((nbLevel-1)/5)),cols=8;for(let r=0;r<rows;r++)for(let c=0;c<cols;c++){let pattern=(r*7+c*3+nbLevel)%11;if(nbLevel%4===0&&pattern===0)continue;nbBricks.push({x:9+c*43,y:65+r*25,w:39,h:18,hp:pattern===1?2:1,max:pattern===1?2:1,color:nbColors[(r+c+nbLevel)%nbColors.length],type:pattern===0?'explosive':'normal'});}}
function breakoutInit(){nbRenderMeta();nbDraw();}
function breakoutSetLevel(n){if(n>nbSave.unlocked)return;breakoutStop();nbLevel=n;nbScore=0;nbLives=3;nbEffects={wide:0,slow:0,laser:0};nbResetStage();nbMessage='Level '+n+' ready';nbUpdateHud();nbDraw();nbRenderMeta();}
function breakoutToggle(){if(nbRunning){breakoutPause();return;}if(nbLevelWon){breakoutNext();return;}if(!nbBalls.length||nbLives<=0)breakoutRestart();nbRunning=true;nbPaused=false;nbMessage='Game running';document.getElementById('nb-start').textContent='RUNNING';nbLast=0;nbFrame=requestAnimationFrame(breakoutLoop);nbUpdateHud();}
function breakoutPause(){if(!nbRunning)return;nbRunning=false;nbPaused=true;cancelAnimationFrame(nbFrame);nbMessage='Paused';document.getElementById('nb-start').textContent='RESUME';nbDraw();nbUpdateHud();}
function breakoutStop(){if(nbRunning){nbRunning=false;cancelAnimationFrame(nbFrame);}nbPaused=false;}
function breakoutRestart(){breakoutStop();nbScore=0;nbLives=3;nbEffects={wide:0,slow:0,laser:0};nbResetStage();nbMessage='Ready';document.getElementById('nb-start').textContent='START GAME';nbUpdateHud();nbDraw();}
function breakoutMove(dir){nbMove=dir;}
function nbUpdateHud(){const el=id=>document.getElementById(id);if(!el('nb-score'))return;el('nb-score').textContent=nbScore;el('nb-lives').textContent=nbLives;el('nb-level-label').textContent='LEVEL '+String(nbLevel).padStart(2,'0')+' / 30';el('nb-status').textContent=nbMessage;el('nb-start').textContent=nbRunning?'RUNNING':nbPaused?'RESUME':nbLevelWon?'NEXT LEVEL':'START GAME';}
function nbDrop(x,y){if(Math.random()>.23)return;const types=['wide','slow','multi','laser'];nbDrops.push({x,y,type:types[Math.floor(Math.random()*types.length)],vy:1.7});}
function nbApplyDrop(d){mobileSfx('coin');if(d.type==='wide'){nbEffects.wide=600;nbPaddle.w=92;}if(d.type==='slow')nbEffects.slow=600;if(d.type==='laser')nbEffects.laser=600;if(d.type==='multi'){const b=nbBalls[0];if(b)for(let i=0;i<2;i++)nbBalls.push({x:b.x,y:b.y,vx:i? -b.vx:b.vx,vy:b.vy,r:6,stuck:false});}nbMessage=({wide:'WIDE PADDLE!',slow:'SLOW BALL!',laser:'LASER READY!',multi:'MULTI-BALL!'}[d.type]);}
function nbHitBrick(index){const b=nbBricks[index];if(!b)return;b.hp--;if(b.hp<=0){nbScore+=b.type==='explosive'?35:10;nbCoins+=1;nbSave.coins+=1;nbDrop(b.x+b.w/2,b.y+b.h/2);nbBricks.splice(index,1);if(b.type==='explosive'){for(let i=nbBricks.length-1;i>=0;i--){const q=nbBricks[i];if(Math.hypot(q.x-b.x,q.y-b.y)<72){nbScore+=8;nbBricks.splice(i,1);}}}}else nbScore+=3;}
function breakoutLoop(t){if(!nbRunning)return;const dt=Math.min(2,(t-(nbLast||t))/16.67||1);nbLast=t;const speed=4.1*(nbEffects.slow>0?.65:1);if(nbMove)nbPaddle.x+=nbMove*5.5*dt;nbPaddle.x=Math.max(0,Math.min(NB_W-nbPaddle.w,nbPaddle.x));if(nbEffects.wide>0)nbEffects.wide-=dt;else nbPaddle.w=60;if(nbEffects.slow>0)nbEffects.slow-=dt;if(nbEffects.laser>0)nbEffects.laser-=dt;
 for(const b of nbBalls){if(b.stuck){b.x=nbPaddle.x+nbPaddle.w/2;b.y=NB_H-65;continue;}b.x+=b.vx*dt*speed/4.1;b.y+=b.vy*dt*speed/4.1;if(b.x<b.r||b.x>NB_W-b.r)b.vx*=-1;if(b.y<b.r+25)b.vy=Math.abs(b.vy);if(b.y>NB_H-58&&b.y<NB_H-43&&b.x>nbPaddle.x&&b.x<nbPaddle.x+nbPaddle.w&&b.vy>0){b.vy=-Math.abs(b.vy);b.vx=((b.x-(nbPaddle.x+nbPaddle.w/2))/(nbPaddle.w/2))*3.8;}
  for(let i=nbBricks.length-1;i>=0;i--){const q=nbBricks[i];if(b.x+b.r>q.x&&b.x-b.r<q.x+q.w&&b.y+b.r>q.y&&b.y-b.r<q.y+q.h){b.vy*=-1;nbHitBrick(i);break;}}}
 nbBalls=nbBalls.filter(b=>b.y<NB_H+15);if(!nbBalls.length){nbLives--;if(nbLives<=0){mobileSfx('gameover');nbRunning=false;nbMessage='GAME OVER · Restart to try again';nbSave.best=Math.max(nbSave.best,nbScore);nbPersist();}else{nbBalls=[{x:nbPaddle.x+nbPaddle.w/2,y:NB_H-65,vx:2.2,vy:-3.4,r:6,stuck:true}];nbMessage='Life lost · Tap to launch';}}
 for(const d of nbDrops){d.y+=d.vy*dt;if(d.y>NB_H-65&&d.y<NB_H-45&&d.x>nbPaddle.x&&d.x<nbPaddle.x+nbPaddle.w)nbApplyDrop(d);}nbDrops=nbDrops.filter(d=>d.y<NB_H+10);
 if(nbEffects.laser>0&&Math.floor(t/160)%4===0){nbLasers.push({x:nbPaddle.x+nbPaddle.w*.25,y:NB_H-70},{x:nbPaddle.x+nbPaddle.w*.75,y:NB_H-70});}for(const l of nbLasers)l.y-=8*dt;nbLasers=nbLasers.filter(l=>l.y>35);for(let i=nbLasers.length-1;i>=0;i--){const l=nbLasers[i],j=nbBricks.findIndex(b=>l.x>=b.x&&l.x<=b.x+b.w&&l.y>=b.y&&l.y<=b.y+b.h);if(j>=0){nbHitBrick(j);nbLasers.splice(i,1);}}
 if(!nbBricks.length&&!nbLevelWon){mobileSfx('success');nbLevelWon=true;nbRunning=false;nbSave.cleared=Array.from(new Set([...nbSave.cleared,nbLevel]));nbSave.unlocked=Math.max(nbSave.unlocked,Math.min(30,nbLevel+1));nbSave.best=Math.max(nbSave.best,nbScore);nbSave.coins=nbCoins;nbPersist();nbMessage=nbLevel===30?'ALL 30 LEVELS CLEARED!':'STAGE CLEAR · NEXT LEVEL UNLOCKED';}
 nbDraw();nbUpdateHud();if(nbRunning)nbFrame=requestAnimationFrame(breakoutLoop);}
function breakoutNext(){if(nbLevel<30){nbLevel++;breakoutRestart();breakoutToggle();}}
function nbDraw(){if(!nbCtx)return;const c=nbCtx;const g=c.createLinearGradient(0,0,0,NB_H);g.addColorStop(0,'#0b1730');g.addColorStop(1,'#070914');c.fillStyle=g;c.fillRect(0,0,NB_W,NB_H);for(let i=0;i<55;i++){c.fillStyle='rgba(180,225,255,'+(0.12+(i%4)*.05)+')';c.fillRect((i*67)%NB_W,(i*97)%NB_H,1.4,1.4);}c.fillStyle='#8ceeff';c.font='bold 10px Arial';c.fillText('NEON SECTOR  '+String(nbLevel).padStart(2,'0'),12,18);for(const b of nbBricks){c.shadowBlur=12;c.shadowColor=b.color;c.fillStyle=b.color;c.beginPath();c.roundRect(b.x,b.y,b.w,b.h,5);c.fill();c.shadowBlur=0;c.fillStyle='#07111f';c.font='bold 9px Arial';c.textAlign='center';c.fillText(b.hp>1?'Ⅱ':b.type==='explosive'?'✹':'',b.x+b.w/2,b.y+12);}c.textAlign='left';for(const d of nbDrops){c.fillStyle=({wide:'#72f28d',slow:'#59caff',multi:'#c28aff',laser:'#ffb45d'}[d.type]);c.shadowBlur=10;c.shadowColor=c.fillStyle;c.beginPath();c.arc(d.x,d.y,7,0,Math.PI*2);c.fill();c.shadowBlur=0;}for(const l of nbLasers){c.fillStyle='#ffad55';c.fillRect(l.x-2,l.y,4,12);}c.shadowBlur=16;c.shadowColor='#62f5ff';c.fillStyle='#69efff';c.beginPath();c.roundRect(nbPaddle.x,NB_H-48,nbPaddle.w,10,5);c.fill();c.shadowBlur=0;for(const b of nbBalls){c.shadowBlur=14;c.shadowColor='#fff';c.fillStyle='#fff';c.beginPath();c.arc(b.x,b.y,b.r,0,Math.PI*2);c.fill();c.shadowBlur=0;}if(!nbRunning){c.fillStyle='rgba(3,8,20,.52)';c.fillRect(0,NB_H/2-26,NB_W,52);c.fillStyle='#eafcff';c.font='bold 14px Arial';c.textAlign='center';c.fillText(nbMessage,NB_W/2,NB_H/2+5);c.textAlign='left';}}
document.addEventListener('keydown',e=>{
 const page=document.getElementById('breakout-page');
 if(!page||page.classList.contains('hidden'))return;
 const key=e.key.toLowerCase();
 if(key==='arrowleft'||key==='a'){e.preventDefault();nbMove=-1;}
 else if(key==='arrowright'||key==='d'){e.preventDefault();nbMove=1;}
 else if(key===' '){e.preventDefault();if(!nbRunning)breakoutToggle();if(nbBalls[0]?.stuck)nbBalls[0].stuck=false;}
});
document.addEventListener('keyup',e=>{
 const key=e.key.toLowerCase();
 if(['arrowleft','arrowright','a','d'].includes(key))nbMove=0;
});
if(nbCanvas){nbCanvas.addEventListener('pointerdown',e=>{nbPointer=e.clientX;const b=nbBalls.find(x=>x.stuck);if(b){b.stuck=false;nbMessage='Good luck!';}if(!nbRunning&&!nbLevelWon&&nbLives>0&&nbPaused===false){/* start remains explicit */}});nbCanvas.addEventListener('pointermove',e=>{if(nbPointer===null&&e.buttons===0)return;const r=nbCanvas.getBoundingClientRect();const x=(e.clientX-r.left)*NB_W/r.width;nbPaddle.x=Math.max(0,Math.min(NB_W-nbPaddle.w,x-nbPaddle.w/2));if(nbBalls[0]?.stuck)nbBalls[0].x=nbPaddle.x+nbPaddle.w/2;});nbCanvas.addEventListener('pointerup',()=>nbPointer=null);nbCanvas.addEventListener('pointercancel',()=>nbPointer=null);}
// Replace start button behavior after stage clear with next stage.
const nbStartButton=document.getElementById('nb-start');if(nbStartButton)nbStartButton.addEventListener('click',()=>{if(nbLevelWon)breakoutNext();else if(nbBalls[0]?.stuck)nbBalls[0].stuck=false;});
nbRenderMeta();nbResetStage();nbUpdateHud();nbDraw();
// ================= END NEON BREAKOUT =================




// Music feature removed as requested.


// ================= SHOPPING STORE (LOCAL DEMO) =================
const shopProductSeeds=[
["Clothing","Classic Hoodie","🧥"],["Clothing","Everyday T-Shirt","👕"],["Clothing","Denim Jacket","🧥"],["Clothing","Cotton Kurta","🥻"],["Clothing","Casual Jeans","👖"],["Clothing","Summer Dress","👗"],["Clothing","Sports Shorts","🩳"],["Clothing","Warm Sweater","🧶"],["Clothing","Formal Shirt","👔"],["Clothing","Rain Jacket","🌧️"],
["Shoes","Street Sneakers","👟"],["Shoes","Running Shoes","🥾"],["Shoes","Canvas Shoes","👟"],["Shoes","Leather Loafers","👞"],["Shoes","Sandals","🩴"],["Shoes","Hiking Boots","🥾"],["Shoes","School Shoes","👞"],["Shoes","Slip-on Shoes","👟"],["Shoes","Sports Trainers","👟"],["Shoes","House Slippers","🥿"],
["Electronics","Wireless Headphones","🎧"],["Electronics","Smart Watch","⌚"],["Electronics","Bluetooth Speaker","🔊"],["Electronics","Portable Charger","🔋"],["Electronics","Gaming Mouse","🖱️"],["Electronics","Mechanical Keyboard","⌨️"],["Electronics","Tablet Stand","📱"],["Electronics","USB Desk Fan","🌀"],["Electronics","LED Monitor Light","💡"],["Electronics","Mini Projector","📽️"],
["Accessories","Travel Backpack","🎒"],["Accessories","Classic Wrist Watch","⌚"],["Accessories","Sunglasses","🕶️"],["Accessories","Leather Wallet","👛"],["Accessories","Sports Cap","🧢"],["Accessories","Steel Water Bottle","🍼"],["Accessories","Travel Pouch","🧳"],["Accessories","Card Holder","💳"],["Accessories","Keychain Set","🔑"],["Accessories","Crossbody Bag","👜"],
["Home","Desk Lamp","💡"],["Home","Cozy Cushion","🛋️"],["Home","Wall Clock","🕰️"],["Home","Storage Basket","🧺"],["Home","Coffee Mug","☕"],["Home","Bedsheet Set","🛏️"],["Home","Table Organizer","🗂️"],["Home","Mini Plant Pot","🪴"],["Home","Laundry Hamper","🧺"],["Home","Decorative Mirror","🪞"],
["Beauty","Care Gift Set","🧴"],["Beauty","Face Wash","🫧"],["Beauty","Hand Cream","🧴"],["Beauty","Hair Brush","🪮"],["Beauty","Body Lotion","🧴"],["Beauty","Scented Soap","🧼"],["Beauty","Nail Care Kit","💅"],["Beauty","Shampoo Bottle","🧴"],["Beauty","Lip Balm","💄"],["Beauty","Skin Care Pouch","🧖"],
["Electronics","Wireless Earbuds","🎶"],["Electronics","Phone Tripod","📷"],["Electronics","Power Bank 20000mAh","🔋"],["Electronics","USB-C Hub","🔌"],["Electronics","Smart LED Bulb","💡"],["Electronics","Webcam","📹"],["Electronics","Portable SSD Case","💾"],["Electronics","Bluetooth Keyboard","⌨️"],["Electronics","Gaming Controller","🎮"],["Electronics","Laptop Cooling Pad","💻"],
["Clothing","Graphic Sweatshirt","👚"],["Clothing","Polo T-Shirt","👕"],["Clothing","Track Pants","👖"],["Clothing","Flannel Shirt","👔"],["Clothing","Winter Gloves","🧤"],["Clothing","Baseball Jersey","🥇"],["Clothing","Zip-up Hoodie","🧥"],["Clothing","Cotton Socks Pack","🧦"],["Clothing","Lightweight Scarf","🧣"],["Clothing","Casual Waistcoat","🦺"],
["Home","Non-stick Pan","🍳"],["Home","Glass Water Set","🥛"],["Home","Kitchen Storage Jars","🫙"],["Home","LED String Lights","✨"],["Home","Foldable Stool","🪑"],["Home","Door Mat","🟫"],["Home","Food Container Set","🥡"],["Home","Wall Art Frame","🖼️"],["Home","Desk Calendar","🗓️"],["Home","Reusable Shopping Bags","🛍️"],
["Accessories","Travel Neck Pillow","🛌"],["Accessories","Minimal Bracelet","📿"],["Accessories","Sports Backpack","🎒"],["Accessories","Laptop Sleeve","💼"],["Accessories","Foldable Umbrella","☂️"],["Accessories","Digital Alarm Clock","⏰"],["Accessories","Reusable Lunch Box","🍱"],["Accessories","Gym Duffel Bag","👜"],["Accessories","Insulated Flask","🧋"],["Accessories","Compact Card Case","💳"]
];
const shopPriceSeed=()=>{let x=Date.now()>>>0;return()=>{x=(x*1664525+1013904223)>>>0;return x/4294967296;};};
const shopRandom=shopPriceSeed();
const shopProducts=shopProductSeeds.map((item,index)=>{const base=650+Math.floor(shopRandom()*11400);return{id:index+1,category:item[0],name:item[1],emoji:item[2],price:Math.round(base/10)*10,old:Math.round(base*(1.12+shopRandom()*.28)/10)*10,stock:4+Math.floor(shopRandom()*47),description:`${item[1]} is a handy ${item[0].toLowerCase()} item selected for the Mobile.app demo marketplace. Check the details, add it to your cart, or try the demo buy option.`,rating:(3.7+shopRandom()*1.3).toFixed(1)};});
let shopCategory="All",shopCart={};
const shopMoney=value=>"Rs. "+Number(value).toLocaleString("en-PK");
function shopSetCategory(category,button){shopCategory=category;document.querySelectorAll(".shop-category").forEach(el=>el.classList.remove("active"));if(button)button.classList.add("active");shopRender();}
function shopRender(){const host=$("shop-products");if(!host)return;const query=($("shop-search")?.value||"").trim().toLowerCase();const visible=shopProducts.filter(p=>(shopCategory==="All"||p.category===shopCategory)&&(p.name.toLowerCase().includes(query)||p.category.toLowerCase().includes(query)));$("shop-result-count").textContent=visible.length+" of 100 items";host.innerHTML=visible.map(p=>`<article class="shop-product" role="button" tabindex="0" aria-label="View ${p.name}" onclick="shopShowDetails(${p.id})" onkeydown="if(event.key==='Enter'||event.key===' '){event.preventDefault();shopShowDetails(${p.id})}"><div class="shop-product-art" aria-hidden="true">${p.emoji}</div><div class="shop-category-name">${p.category.toUpperCase()}</div><h4>${p.name}</h4><div class="shop-price">${shopMoney(p.price)}<span class="shop-old-price">${shopMoney(p.old)}</span></div><button class="shop-add" onclick="event.stopPropagation();shopAdd(${p.id})">＋ ADD TO CART</button></article>`).join("")||'<p class="small-note">No products found. Try another search.</p>';shopUpdateCart();}
function shopShowDetails(id){const p=shopProducts.find(x=>x.id===Number(id));const panel=$("shop-detail");if(!p||!panel)return;panel.innerHTML=`<button class="shop-detail-close" onclick="shopCloseDetails()" aria-label="Close details">✕</button><div class="shop-detail-art">${p.emoji}</div><div class="shop-category-name">${p.category.toUpperCase()} · PRODUCT #${p.id}</div><h3>${p.name}</h3><div class="shop-price">${shopMoney(p.price)} <span class="shop-old-price">${shopMoney(p.old)}</span></div><p>${p.description}</p><p>⭐ ${p.rating}/5 · Demo stock: ${p.stock} available</p><div class="shop-detail-actions"><button class="shop-detail-add" onclick="shopAdd(${p.id});shopCloseDetails()">ADD TO CART</button><button class="shop-detail-buy" onclick="shopBuyNow(${p.id})">BUY NOW</button></div>`;panel.classList.remove("hidden");panel.scrollIntoView({behavior:"smooth",block:"nearest"});}
function shopCloseDetails(){const panel=$("shop-detail");if(panel)panel.classList.add("hidden");}
function shopBuyNow(id){shopAdd(id);shopToggleCart();shopCloseDetails();const msg=$("shop-message");if(msg)msg.textContent="Added to cart. Review your demo order below; no payment is processed.";}

function shopAdd(id){shopCart[id]=(shopCart[id]||0)+1;$("shop-message").textContent="Added to your cart.";shopUpdateCart();}
function shopUpdateCart(){const count=Object.values(shopCart).reduce((a,b)=>a+b,0);const countEl=$("shop-cart-count");if(countEl)countEl.textContent=count;const rows=Object.entries(shopCart).filter(([,qty])=>qty>0);const list=$("shop-cart-items");if(list)list.innerHTML=rows.length?rows.map(([id,qty])=>{const p=shopProducts.find(x=>x.id===Number(id));return `<div class="shop-cart-line"><span>${p.emoji}</span><span>${p.name}<br>${shopMoney(p.price)} × ${qty}</span><b>${shopMoney(p.price*qty)}</b><button onclick="shopRemove(${id})" aria-label="Remove one">−</button></div>`;}).join(""):'<p class="small-note">Your cart is empty.</p>';const total=rows.reduce((sum,[id,qty])=>sum+shopProducts.find(p=>p.id===Number(id)).price*qty,0);const totalEl=$("shop-total");if(totalEl)totalEl.textContent=shopMoney(total);}
let shopOrderHistory=store.get("mobile_shop_orders",[]);
function shopRemove(id){if(!shopCart[id])return;shopCart[id]--;if(shopCart[id]<=0)delete shopCart[id];shopUpdateCart();if($("shop-order-page")&&!$("shop-order-page").classList.contains("hidden"))shopRenderOrderPage();}
function shopToggleCart(){shopUpdateCart();shopRenderOrderPage();showPage("shop-order-page");}
function shopRenderOrderPage(){
 const rows=Object.entries(shopCart).filter(([,qty])=>qty>0);
 const lineHost=$("shop-order-cart-lines"),countHost=$("shop-order-item-count"),totalHost=$("shop-order-total");
 const count=rows.reduce((sum,[,qty])=>sum+qty,0);
 if(countHost)countHost.textContent=count+" item"+(count===1?"":"s");
 if(lineHost)lineHost.innerHTML=rows.length?rows.map(([id,qty])=>{const p=shopProducts.find(x=>x.id===Number(id));return `<div class="shop-order-line"><span style="font-size:25px">${p.emoji}</span><span class="item-main"><b>${p.name}</b><small>${shopMoney(p.price)} × ${qty}</small></span><b>${shopMoney(p.price*qty)}</b><button onclick="shopRemove(${id})" aria-label="Remove one item" style="padding:6px 9px;border-radius:8px;background:#ffffff22;color:#fff">−</button><button onclick="shopAdd(${id});shopRenderOrderPage()" aria-label="Add one item" style="padding:6px 9px;border-radius:8px;background:#ffffff22;color:#fff">＋</button></div>`;}).join(""):'<p class="shop-order-muted">Your cart is empty. Return to the store and add products.</p>';
 const total=rows.reduce((sum,[id,qty])=>sum+shopProducts.find(p=>p.id===Number(id)).price*qty,0);
 if(totalHost)totalHost.textContent=shopMoney(total);
 const historyHost=$("shop-order-history"),historyCount=$("shop-history-count");
 if(historyCount)historyCount.textContent=shopOrderHistory.length+" order"+(shopOrderHistory.length===1?"":"s");
 if(historyHost)historyHost.innerHTML=shopOrderHistory.length?shopOrderHistory.slice().reverse().map(order=>`<div class="shop-history-entry"><div style="display:flex;justify-content:space-between;gap:8px"><b>${order.id}</b><b>${shopMoney(order.total)}</b></div><div style="margin-top:5px;color:#d6e3f1">${order.date} · ${order.status}</div><div style="margin-top:5px">${order.items.map(item=>`${item.emoji} ${item.name} × ${item.qty}`).join(" · ")}</div></div>`).join(""):'<p class="shop-order-muted">No demo orders yet. Your order will appear here after you place it.</p>';
}
function shopCheckout(){
 const rows=Object.entries(shopCart).filter(([,qty])=>qty>0);
 const count=rows.reduce((sum,[,qty])=>sum+qty,0);
 const message=$("shop-order-message");
 if(!count){if(message)message.textContent="Your cart is empty. Add products before placing an order.";return;}
 const items=rows.map(([id,qty])=>{const p=shopProducts.find(x=>x.id===Number(id));return{id:p.id,name:p.name,emoji:p.emoji,price:p.price,qty};});
 const total=items.reduce((sum,item)=>sum+item.price*item.qty,0);
 const order={id:"MOB-"+String(Date.now()).slice(-8),date:new Date().toLocaleString(),items,total,status:"Demo order placed"};
 shopOrderHistory.push(order);store.set("mobile_shop_orders",shopOrderHistory);
 shopCart={};shopUpdateCart();shopRenderOrderPage();
 if(message)message.textContent="✓ Demo order placed successfully! Your order is now saved in Order history on this device.";
 const shopMessage=$("shop-message");if(shopMessage)shopMessage.textContent="Your demo order has been placed.";
}
// ================= END SHOPPING STORE =================




// ================= HOUSE DESIGNER =================
const HD_W=900,HD_H=620,HD_SCALE=1;
let hdRooms=[],hdItems=[],hdOpenings=[],hdSelected=null,hdView='plan',hdZoomLevel=1,hdDrag=null,hdUndoStack=[];
const hdRoomStyles={'Living Room':'#d8c5a8','Bedroom':'#c7d8e7','Kitchen':'#d8d2ad','Bathroom':'#b9d9d8','Dining':'#dec7b1','Study':'#c9c2df'};
const hdFurniture={'Sofa':['🛋️',105,48,'#9b7890'],'Bed':['🛏️',112,76,'#d2b9a2'],'Table':['▱',72,52,'#b78a5c'],'Chair':['◉',34,34,'#8a9b9f'],'Wardrobe':['▤',75,35,'#9b806a'],'Plant':['🪴',35,35,'#75a67a'],'Kitchen':['▰',110,38,'#a5a6a0'],'Shower':['🚿',48,48,'#8bbdc5'],'TV':['▰',70,18,'#333b48'],'Lamp':['💡',28,28,'#e9c96f'],'Door':['🚪',54,12,'#a87951'],'Window':['▥',58,12,'#77b9d0']};
function hdCanvas(){return $('hd-canvas')}
function hdStatus(t){const e=$('hd-status');if(e)e.textContent=t;}
function hdSnapshot(){hdUndoStack.push(JSON.stringify({rooms:hdRooms,items:hdItems,openings:hdOpenings}));if(hdUndoStack.length>25)hdUndoStack.shift();}
function hdInit(){if(!hdCanvas()||hdCanvas().__hdReady)return;hdCanvas().__hdReady=true;hdCanvas().addEventListener('pointerdown',hdPointerDown);hdCanvas().addEventListener('pointermove',hdPointerMove);window.addEventListener('pointerup',hdPointerUp);hdRender();}
function hdAddRoom(name){hdSnapshot();const n=hdRooms.length;const room={id:'r'+Date.now()+Math.random(),name,x:70+(n%3)*245,y:75+Math.floor(n/3)*205,w:210,h:155,color:hdRoomStyles[name]||'#d8c5a8',rotation:0};hdRooms.push(room);hdSelected={type:'room',id:room.id};hdRender();hdSyncSelection();hdStatus(name+' added. Drag it to position.');}
function hdAddItem(name){hdSnapshot();const f=hdFurniture[name]||['•',50,40,'#aaa'];const item={id:'i'+Date.now()+Math.random(),name,x:120+Math.random()*500,y:130+Math.random()*300,w:f[1],h:f[2],color:f[3],rotation:0,emoji:f[0]};hdItems.push(item);hdSelected={type:'item',id:item.id};hdRender();hdSyncSelection();hdStatus(name+' added to your plan.');}
function hdAddOpening(name){hdSnapshot();const f=hdFurniture[name];const item={id:'o'+Date.now()+Math.random(),name,x:260+Math.random()*300,y:300,w:f[1],h:f[2],color:f[3],rotation:0,emoji:f[0]};hdOpenings.push(item);hdSelected={type:'opening',id:item.id};hdRender();hdSyncSelection();hdStatus(name+' marker added.');}
function hdFind(){if(!hdSelected)return null;const list=hdSelected.type==='room'?hdRooms:hdSelected.type==='opening'?hdOpenings:hdItems;return list.find(x=>x.id===hdSelected.id)||null;}
function hdUpdateSelected(key,value){const o=hdFind();if(!o)return;if(key==='w'||key==='h'){const v=Number(value);if(!Number.isFinite(v)||v<0.5)return;o[key]=Math.max(22,Math.min(700,v*44));}else o[key]=value;hdRender();}
function hdSyncSelection(){const o=hdFind(),empty=$('hd-selection-empty'),edit=$('hd-selection-edit');if(!o){empty?.classList.remove('hidden');edit?.classList.add('hidden');$('hd-selection-type').textContent='NOTHING SELECTED';return;}empty?.classList.add('hidden');edit?.classList.remove('hidden');$('hd-selection-type').textContent=hdSelected.type.toUpperCase();$('hd-name').value=o.name;$('hd-width').value=(o.w/44).toFixed(1);$('hd-height').value=(o.h/44).toFixed(1);$('hd-color').value=o.color||'#d8b18a';}
function hdDeleteSelected(){if(!hdSelected)return;hdSnapshot();const list=hdSelected.type==='room'?hdRooms:hdSelected.type==='opening'?hdOpenings:hdItems;const i=list.findIndex(x=>x.id===hdSelected.id);if(i>=0)list.splice(i,1);hdSelected=null;hdRender();hdSyncSelection();hdStatus('Selected element deleted.');}
function hdRotateSelected(){const o=hdFind();if(!o)return;hdSnapshot();o.rotation=((o.rotation||0)+90)%360;hdRender();}
function hdHit(x,y){for(const [type,list] of [['opening',hdOpenings],['item',hdItems],['room',hdRooms]])for(let i=list.length-1;i>=0;i--){const o=list[i];if(x>=o.x&&x<=o.x+o.w&&y>=o.y&&y<=o.y+o.h)return{type,id:o.id};}return null;}
function hdPoint(e){const r=hdCanvas().getBoundingClientRect();const sx=(e.clientX-r.left)/r.width*HD_W,sy=(e.clientY-r.top)/r.height*HD_H;return{x:(sx-HD_W/2)/hdZoomLevel+HD_W/2,y:(sy-HD_H/2)/hdZoomLevel+HD_H/2};}
function hdPointerDown(e){if(hdView!=='plan')return;const p=hdPoint(e),hit=hdHit(p.x,p.y);hdSelected=hit;if(hit){hdSnapshot();hdDrag={x:p.x,y:p.y,obj:hdFind(),ox:hdFind().x,oy:hdFind().y};hdCanvas().setPointerCapture(e.pointerId);}hdRender();hdSyncSelection();}
function hdPointerMove(e){if(!hdDrag)return;const p=hdPoint(e);hdDrag.obj.x=Math.max(8,Math.min(HD_W-hdDrag.obj.w-8,hdDrag.ox+p.x-hdDrag.x));hdDrag.obj.y=Math.max(8,Math.min(HD_H-hdDrag.obj.h-8,hdDrag.oy+p.y-hdDrag.y));hdRender();}
function hdPointerUp(){hdDrag=null;}
function hdDrawGrid(ctx){ctx.fillStyle='#eee8dc';ctx.fillRect(0,0,HD_W,HD_H);ctx.strokeStyle='#d8d0c2';ctx.lineWidth=1;for(let x=0;x<=HD_W;x+=22){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,HD_H);ctx.stroke();}for(let y=0;y<=HD_H;y+=22){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(HD_W,y);ctx.stroke();}}
function hdDrawRoom(ctx,r){ctx.save();ctx.translate(r.x+r.w/2,r.y+r.h/2);ctx.rotate((r.rotation||0)*Math.PI/180);ctx.fillStyle=r.color;ctx.globalAlpha=.76;ctx.fillRect(-r.w/2,-r.h/2,r.w,r.h);ctx.globalAlpha=1;ctx.strokeStyle='#55483d';ctx.lineWidth=7;ctx.strokeRect(-r.w/2,-r.h/2,r.w,r.h);ctx.fillStyle='#51463d';ctx.font='bold 17px Arial';ctx.textAlign='center';ctx.fillText(r.name,0,0);ctx.font='11px Arial';ctx.fillStyle='#77695d';ctx.fillText((r.w/44).toFixed(1)+'m × '+(r.h/44).toFixed(1)+'m',0,18);ctx.restore();if(hdSelected?.id===r.id){ctx.strokeStyle='#2479c8';ctx.lineWidth=4;ctx.setLineDash([8,5]);ctx.strokeRect(r.x-4,r.y-4,r.w+8,r.h+8);ctx.setLineDash([]);}}
function hdDrawItem(ctx,o,type){ctx.save();ctx.translate(o.x+o.w/2,o.y+o.h/2);ctx.rotate((o.rotation||0)*Math.PI/180);ctx.fillStyle=o.color||'#aaa';ctx.strokeStyle='#51483f';ctx.lineWidth=2;ctx.fillRect(-o.w/2,-o.h/2,o.w,o.h);ctx.strokeRect(-o.w/2,-o.h/2,o.w,o.h);ctx.fillStyle=type==='opening'?'#273c4d':'#27323a';ctx.font='bold 13px Arial';ctx.textAlign='center';ctx.textBaseline='middle';ctx.fillText(o.emoji||'•',0,-2);ctx.font='10px Arial';ctx.fillText(o.name,0,o.h/2+12);ctx.restore();if(hdSelected?.id===o.id){ctx.strokeStyle='#1679d0';ctx.lineWidth=3;ctx.setLineDash([5,4]);ctx.strokeRect(o.x-4,o.y-4,o.w+8,o.h+8);ctx.setLineDash([]);}}
function hdRenderPlan(ctx){hdDrawGrid(ctx);ctx.fillStyle='#9d8e7a';ctx.font='bold 15px Arial';ctx.fillText('FLOOR PLAN · 1 GRID = 0.5 m',20,27);hdRooms.forEach(r=>hdDrawRoom(ctx,r));hdItems.forEach(o=>hdDrawItem(ctx,o,'item'));hdOpenings.forEach(o=>hdDrawItem(ctx,o,'opening'));if(!hdRooms.length){ctx.fillStyle='#887e72';ctx.textAlign='center';ctx.font='bold 22px Arial';ctx.fillText('Your home starts here',HD_W/2,HD_H/2-8);ctx.font='14px Arial';ctx.fillText('Add rooms below to create your floor plan',HD_W/2,HD_H/2+20);ctx.textAlign='left';}}
function hdIso(ctx,x,y,z){return{x:(x-y)*.72+450,y:(x+y)*.38-z+110};}
function hdPoly(ctx,pts,fill,stroke='#5c5148'){ctx.beginPath();pts.forEach((p,i)=>i?ctx.lineTo(p.x,p.y):ctx.moveTo(p.x,p.y));ctx.closePath();ctx.fillStyle=fill;ctx.fill();ctx.strokeStyle=stroke;ctx.lineWidth=2;ctx.stroke();}
function hdRender3D(ctx){ctx.fillStyle='#dce8ed';ctx.fillRect(0,0,HD_W,HD_H);const rooms=hdRooms.length?hdRooms:[{x:170,y:160,w:480,h:300,name:'Your Home',color:'#d8c5a8'}];rooms.forEach(r=>{const x=r.x/1.5,y=r.y/1.5,w=r.w/1.5,h=r.h/1.5,z=75;const a=hdIso(ctx,x,y,0),b=hdIso(ctx,x+w,y,0),c=hdIso(ctx,x+w,y+h,0),d=hdIso(ctx,x,y+h,0),a2=hdIso(ctx,x,y,z),b2=hdIso(ctx,x+w,y,z),d2=hdIso(ctx,x,y+h,z);hdPoly(ctx,[a,b,c,d],'#b69a79');hdPoly(ctx,[a,b,b2,a2],'#e5d8c5');hdPoly(ctx,[a,d,d2,a2],'#cbb99f');hdPoly(ctx,[a2,b2,hdIso(ctx,x+w,y+h,z),d2],r.color||'#d8c5a8','#77685a');ctx.fillStyle='#403a35';ctx.font='bold 14px Arial';ctx.textAlign='center';const label=hdIso(ctx,x+w/2,y+h/2,z+2);ctx.fillText(r.name,label.x,label.y);});hdItems.forEach(o=>{const q=hdIso(ctx,o.x/1.5+o.w/3,o.y/1.5+o.h/3,18);ctx.fillStyle=o.color||'#999';ctx.fillRect(q.x-14,q.y-10,28,20);ctx.strokeStyle='#554';ctx.strokeRect(q.x-14,q.y-10,28,20);ctx.fillStyle='#28343c';ctx.font='12px Arial';ctx.textAlign='center';ctx.fillText(o.emoji||'•',q.x,q.y+4);});ctx.fillStyle='#42596a';ctx.font='bold 15px Arial';ctx.textAlign='left';ctx.fillText('ISOMETRIC 3D-STYLE PREVIEW',20,28);ctx.font='11px Arial';ctx.fillText('Concept view · room layout and furniture arrangement',20,48);}
function hdRender(){const c=hdCanvas();if(!c)return;const ctx=c.getContext('2d');ctx.save();ctx.clearRect(0,0,HD_W,HD_H);ctx.translate(HD_W/2,HD_H/2);ctx.scale(hdZoomLevel,hdZoomLevel);ctx.translate(-HD_W/2,-HD_H/2);if(hdView==='3d')hdRender3D(ctx);else hdRenderPlan(ctx);ctx.restore();$('hd-tab-plan')?.classList.toggle('active',hdView==='plan');$('hd-tab-3d')?.classList.toggle('active',hdView==='3d');$('hd-canvas-hint').textContent=hdView==='plan'?'Tap an object to select · Drag to move · Use controls to edit':'Isometric preview of your current rooms and furniture';$('hd-room-count').textContent=hdRooms.length;$('hd-item-count').textContent=hdItems.length+hdOpenings.length;$('hd-area').textContent=Math.round(hdRooms.reduce((a,r)=>a+(r.w/44)*(r.h/44),0));}
function hdSetView(v){hdView=v;hdRender();}
function hdZoom(d){hdZoomLevel=Math.max(.65,Math.min(1.35,hdZoomLevel+d*.1));hdRender();}
function hdSave(){try{localStorage.setItem('mobile_app_house_design',JSON.stringify({rooms:hdRooms,items:hdItems,openings:hdOpenings}));hdStatus('Design saved on this device.');}catch(e){hdStatus('Could not save. Device storage may be unavailable.');}}
function hdLoad(){try{const raw=localStorage.getItem('mobile_app_house_design');if(!raw){hdStatus('No saved design found on this device.');return;}const d=JSON.parse(raw);hdRooms=Array.isArray(d.rooms)?d.rooms:[];hdItems=Array.isArray(d.items)?d.items:[];hdOpenings=Array.isArray(d.openings)?d.openings:[];hdSelected=null;hdRender();hdSyncSelection();hdStatus('Saved design loaded.');}catch(e){hdStatus('Saved design could not be read.');}}
function hdUndo(){const raw=hdUndoStack.pop();if(!raw){hdStatus('Nothing to undo yet.');return;}const d=JSON.parse(raw);hdRooms=d.rooms;hdItems=d.items;hdOpenings=d.openings;hdSelected=null;hdRender();hdSyncSelection();hdStatus('Last change undone.');}
function hdNew(){if(!confirm('Start a new house plan? Unsaved changes will be cleared.'))return;hdSnapshot();hdRooms=[];hdItems=[];hdOpenings=[];hdSelected=null;hdRender();hdSyncSelection();hdStatus('New empty plan created.');}
function hdExport(){const c=hdCanvas();if(!c)return;const a=document.createElement('a');a.download='mobile-app-house-design.png';a.href=c.toDataURL('image/png');a.click();hdStatus('Plan image exported.');}
// ================= END HOUSE DESIGNER =================

// INITIAL SETUP

resetGuess();
shopRender();
resetSnake();
drawFlappy();
drawCar();
renderNotes();
showPage("login-page");


// ================= QURAN READER =================
const QURAN_API = "https://api.alquran.cloud/v1";
const QURAN_RECITERS = {
  "Mishary Alafasy": "https://server8.mp3quran.net/afs/{n}.mp3",
  "Abdul Basit (Murattal)": "https://server7.mp3quran.net/basit/{n}.mp3",
  "Abdurrahman As-Sudais": "https://server11.mp3quran.net/sds/{n}.mp3",
  "Saud Ash-Shuraim": "https://server7.mp3quran.net/shur/{n}.mp3",
  "Maher Al-Muaiqly": "https://server12.mp3quran.net/maher/{n}.mp3"
};
let quranSurahList = [];
let quranLoadedSurah = 0;
let quranRequestToken = 0;
let quranAyahAudioData = null;

function quranEscape(value) {
  return String(value ?? "").replace(/[&<>"']/g, ch => ({
    "&":"&amp;", "<":"&lt;", ">":"&gt;", '"':"&quot;", "'":"&#39;"
  })[ch]);
}

async function initQuranReader() {
  const status = $("quran-status");
  if (quranSurahList.length) {
    if (!quranLoadedSurah) loadQuranSurah();
    return;
  }
  status.textContent = "Loading surah list...";
  try {
    const response = await fetch(QURAN_API + "/surah");
    if (!response.ok) throw new Error("HTTP " + response.status);
    const result = await response.json();
    quranSurahList = result.data || [];
    const select = $("quran-surah");
    select.innerHTML = quranSurahList.map(s =>
      `<option value="${s.number}">${s.number}. ${quranEscape(s.englishName)} (${quranEscape(s.name)})</option>`
    ).join("");
    status.textContent = "Surah list loaded.";
    loadQuranSurah();
  } catch (error) {
    status.textContent = "Could not load surah list. Check your internet connection. " + error.message;
  }
}

function updateQuranFullAudio() {
  if (!quranLoadedSurah) return;
  const template = $("quran-reciter").value;
  const source = template.replace("{n}", String(quranLoadedSurah).padStart(3, "0"));
  const player = $("quran-full-audio");
  if (player.src !== source) {
    player.src = source;
    player.load();
  }
}

function changeQuranFont(value) {
  $("quran-font-label").textContent = Number(value).toFixed(1);
  document.querySelectorAll("#quran-content .quran-arabic").forEach(el => {
    el.style.fontSize = value + "rem";
    el.style.lineHeight = (Number(value) * 1.6) + "rem";
  });
}

function toggleQuranAyahAudio() {
  if (quranLoadedSurah) renderQuranAyahAudio();
}

function renderQuranAyahAudio() {
  const enabled = $("quran-ayah-audio").checked;
  document.querySelectorAll("#quran-content .quran-ayah-audio-slot").forEach((slot, index) => {
    if (!enabled || !quranAyahAudioData || !quranAyahAudioData[index]) {
      slot.innerHTML = "";
      return;
    }
    const audioUrl = quranAyahAudioData[index].audio;
    slot.innerHTML = audioUrl ? `<audio controls preload="none" src="${quranEscape(audioUrl)}"></audio>` : "";
  });
}

async function loadQuranSurah() {
  if (!quranSurahList.length) return;
  const number = Number($("quran-surah").value || 1);
  const translation = $("quran-translation").value;
  const token = ++quranRequestToken;
  const status = $("quran-status");
  const content = $("quran-content");
  status.textContent = "Loading surah...";
  content.innerHTML = "";
  quranLoadedSurah = number;
  updateQuranFullAudio();

  const editions = "quran-uthmani,ar.alafasy" + (translation ? "," + translation : "");
  try {
    const response = await fetch(`${QURAN_API}/surah/${number}/editions/${editions}`);
    if (!response.ok) throw new Error("HTTP " + response.status);
    const result = await response.json();
    if (token !== quranRequestToken) return;
    const data = result.data || [];
    const arabic = data.find(d => d.edition.identifier === "quran-uthmani");
    const audio = data.find(d => d.edition.identifier === "ar.alafasy");
    const trans = data.find(d => d.edition.type === "translation") || null;
    if (!arabic || !audio) throw new Error("Required Quran editions were not returned.");

    const meta = quranSurahList[number - 1];
    $("quran-surah-heading").textContent = meta.englishName + " — " + meta.name;
    $("quran-surah-meta").textContent = `${meta.englishNameTranslation} • ${meta.numberOfAyahs} ayahs • ${meta.revelationType}`;
    quranAyahAudioData = audio.ayahs || [];

    let html = "";
    if (number !== 1 && number !== 9) {
      html += '<div class="quran-bismillah">بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ</div>';
    }
    arabic.ayahs.forEach((ayah, index) => {
      let text = ayah.text;
      if (number !== 1 && index === 0) {
        const bism = "بِسْمِ ٱللَّهِ ٱلرَّحْمَـٰنِ ٱلرَّحِيمِ";
        if (text.startsWith(bism)) text = text.slice(bism.length).trim();
      }
      const ayahNumber = ayah.numberInSurah;
      const translationText = trans && trans.ayahs[index] ? trans.ayahs[index].text : "";
      html += `<div class="quran-ayah"><div class="quran-arabic" style="font-size:${$("quran-font-size").value}rem;line-height:${Number($("quran-font-size").value)*1.6}rem">${quranEscape(text)} ﴿${ayahNumber}﴾</div>`;
      if (translationText) html += `<div class="quran-translation">${quranEscape(translationText)}</div>`;
      html += `<div class="quran-ayah-audio-slot"></div></div>`;
    });
    content.innerHTML = html;
    renderQuranAyahAudio();
    status.textContent = "Surah loaded successfully.";
  } catch (error) {
    if (token !== quranRequestToken) return;
    status.textContent = "Could not load surah text. " + error.message;
  }
}
// ================= END QURAN READER =================

// ================= SOLAR SYSTEM EXPLORER =================
const solarData = {
 mercury:{texture:"https://www.solarsystemscope.com/textures/download/2k_mercury.jpg",name:"Mercury",type:"TERRESTRIAL PLANET",distance:"0.39 AU FROM THE SUN",year:"88 Earth days",day:"58.6 Earth days",size:"4,879 km",temp:"167°C",color:"radial-gradient(circle at 30% 25%,#e4e0d8,#77736e 65%,#292a31)",description:"Mercury is the smallest planet and the closest to the Sun. Its ancient, heavily cratered surface records billions of years of impacts. It has almost no atmosphere to retain heat, so temperatures vary dramatically between day and night.",moons:["No natural moons"]},
 venus:{texture:"https://www.solarsystemscope.com/textures/download/2k_venus_surface.jpg",name:"Venus",type:"TERRESTRIAL PLANET",distance:"0.72 AU FROM THE SUN",year:"225 Earth days",day:"243 Earth days",size:"12,104 km",temp:"464°C",color:"radial-gradient(circle at 30% 25%,#fff0bd,#d18a45 55%,#74401e)",description:"Venus is wrapped in thick clouds of sulfuric acid droplets. Its atmosphere is mostly carbon dioxide, creating an intense greenhouse effect that makes its surface hotter than Mercury's. It rotates slowly in the opposite direction to most planets.",moons:["No natural moons"]},
 earth:{texture:"https://www.solarsystemscope.com/textures/download/2k_earth_daymap.jpg",name:"Earth",type:"TERRESTRIAL PLANET",distance:"1 AU FROM THE SUN",year:"365.25 days",day:"23 h 56 min",size:"12,742 km",temp:"15°C",color:"radial-gradient(circle at 30% 25%,#d5f8ff 0 8%,#46b7e7 25%,#1765a5 58%,#082b59 82%)",description:"Earth is the only world currently known to support life. Its surface has vast oceans of liquid water, active geology and a protective magnetic field. Nitrogen and oxygen dominate its atmosphere, while clouds and weather continually reshape the view from space.",moons:["The Moon"]},
 mars:{texture:"https://www.solarsystemscope.com/textures/download/2k_mars.jpg",name:"Mars",type:"TERRESTRIAL PLANET",distance:"1.52 AU FROM THE SUN",year:"687 Earth days",day:"24 h 37 min",size:"6,779 km",temp:"−65°C",color:"radial-gradient(circle at 30% 25%,#ffd1a1,#bd5832 58%,#55251d)",description:"Mars is a cold desert world with a thin carbon-dioxide atmosphere. Its surface contains enormous volcanoes, deep canyons, ancient river channels and polar ice caps. Robotic explorers study whether liquid water once persisted there for long periods.",moons:["Phobos","Deimos"]},
 jupiter:{texture:"https://www.solarsystemscope.com/textures/download/2k_jupiter.jpg",name:"Jupiter",type:"GAS GIANT",distance:"5.20 AU FROM THE SUN",year:"11.86 Earth years",day:"9 h 56 min",size:"139,820 km",temp:"−110°C",color:"repeating-linear-gradient(8deg,#d9b18b 0 7%,#9b684b 8% 13%,#f0d4ac 14% 20%,#a96f4f 21% 27%)",description:"Jupiter is the largest planet, a giant world made mostly of hydrogen and helium. Its colorful cloud bands are shaped by powerful winds, and the Great Red Spot is a giant storm that has persisted for centuries. Jupiter has a large family of moons.",moons:["Io","Europa","Ganymede","Callisto"]},
 saturn:{texture:"https://www.solarsystemscope.com/textures/download/2k_saturn.jpg",name:"Saturn",type:"GAS GIANT",distance:"9.58 AU FROM THE SUN",year:"29.4 Earth years",day:"10 h 33 min",size:"116,460 km",temp:"−140°C",color:"radial-gradient(circle at 30% 25%,#fff1c8,#c89b62 62%,#725034)",description:"Saturn is a gas giant famous for its spectacular rings, made mostly of countless pieces of water ice with some rocky material. The planet is less dense than water on average. Its moon Titan has lakes and seas of liquid hydrocarbons.",moons:["Titan","Enceladus","Rhea","Dione","Iapetus"]},
 uranus:{texture:"https://www.solarsystemscope.com/textures/download/2k_uranus.jpg",name:"Uranus",type:"ICE GIANT",distance:"19.2 AU FROM THE SUN",year:"84 Earth years",day:"17 h 14 min",size:"50,724 km",temp:"−195°C",color:"radial-gradient(circle at 30% 25%,#e0ffff,#8ad5dc 58%,#397f99)",description:"Uranus is an ice giant with a blue-green appearance caused by methane in its atmosphere. Its rotation axis is tilted by about 98 degrees, so it effectively rolls around the Sun. It has faint rings and a cold, dynamic atmosphere.",moons:["Miranda","Ariel","Umbriel","Titania","Oberon"]},
 neptune:{texture:"https://www.solarsystemscope.com/textures/download/2k_neptune.jpg",name:"Neptune",type:"ICE GIANT",distance:"30.1 AU FROM THE SUN",year:"164.8 Earth years",day:"16 h 6 min",size:"49,244 km",temp:"−200°C",color:"radial-gradient(circle at 30% 25%,#b8dcff,#386fce 58%,#122b78)",description:"Neptune is a distant ice giant with a deep-blue atmosphere and some of the fastest winds measured on any planet. It receives very little sunlight, yet its atmosphere remains active with storms and changing cloud patterns.",moons:["Triton","Proteus","Nereid"]},
 pluto:{name:"Pluto",type:"DWARF PLANET",distance:"39.5 AU FROM THE SUN (AVERAGE)",year:"248 Earth years",day:"6.4 Earth days",size:"2,377 km",temp:"−225°C",color:"radial-gradient(circle at 30% 25%,#f4dfc8,#a78a78 65%,#554a48)",description:"Pluto is a dwarf planet in the Kuiper Belt beyond Neptune. It has mountains of water ice, broad plains of frozen nitrogen and a thin atmosphere that changes as it travels along its elongated orbit. NASA's New Horizons spacecraft flew past it in 2015.",moons:["Charon","Styx","Nix","Kerberos","Hydra"]},
 sun:{texture:null,name:"The Sun",type:"STAR · THE CENTRE OF OUR SOLAR SYSTEM",distance:"0 AU · CENTRAL STAR",year:"About 225 million years per galactic orbit",day:"About 25–35 days (varies by latitude)",size:"1.39 million km",temp:"5,500°C at surface",color:"radial-gradient(circle at 32% 25%,#fffbd0 0 5%,#ffe18a 18%,#ff9a32 52%,#b72d12 100%)",description:"The Sun is a G-type main-sequence star containing about 99.86% of the Solar System's mass. Its energy is produced by nuclear fusion in the core. Sunlight and the solar wind influence every planet and many smaller bodies.",moons:["No moons — planets orbit the Sun"]}
};
let solarMotion=true;
function solarSelect(key){
 const d=solarData[key];if(!d)return;
 const put=(id,value)=>{const el=$(id);if(el)el.textContent=value;};
 put("solar-detail-type",d.type);put("solar-detail-name",d.name);put("solar-detail-distance",d.distance);
 put("solar-detail-description",d.description);put("solar-fact-year",d.year);put("solar-fact-day",d.day);
 put("solar-fact-size",d.size);put("solar-fact-temp",d.temp);
 const orb=$("solar-detail-orb");if(orb){orb.style.backgroundImage=d.texture?`radial-gradient(circle at 30% 25%,#ffffff22 0%,transparent 42%,#0008 100%),url("${d.texture}"),${d.color}`:d.color;orb.style.backgroundColor="#27364a";orb.classList.toggle("sun-selected",key==="sun");}
 const moons=$("solar-moons");if(moons)moons.innerHTML=d.moons.map(m=>'<span class="solar-moon-chip">'+m+'</span>').join("");
 document.querySelectorAll(".solar-pick").forEach(b=>b.classList.remove("selected"));
 const chosen=$("solar-pick-"+key);if(chosen)chosen.classList.add("selected");
}
function solarToggleMotion(){
 solarMotion=!solarMotion;
 document.querySelectorAll(".solar-orbit").forEach(o=>o.style.animationPlayState=solarMotion?"running":"paused");
 const b=$("solar-motion-btn");if(b){b.textContent=solarMotion?"Ⅱ PAUSE ORBITS":"▶ RESUME ORBITS";b.classList.toggle("active",solarMotion);}
}
function solarStop(){}
document.querySelectorAll(".solar-orbit").forEach(o=>o.style.animationPlayState="running");
solarSelect("earth");
// =============== END SOLAR SYSTEM EXPLORER ===============



// ================= MOBILE.APP SOUND ENGINE =================
// All effects are synthesized locally with Web Audio; no sound files or API keys needed.
let mobileAudioContext = null;
let mobileMasterGain = null;
let mobileLastTypeSound = 0;

function mobileAudioReady(){
  const AudioCtor = window.AudioContext || window.webkitAudioContext;
  if(!AudioCtor) return false;
  if(!mobileAudioContext){
    mobileAudioContext = new AudioCtor();
    mobileMasterGain = mobileAudioContext.createGain();
    mobileMasterGain.gain.value = 0.34;
    mobileMasterGain.connect(mobileAudioContext.destination);
  }
  if(mobileAudioContext.state === "suspended") mobileAudioContext.resume().catch(()=>{});
  return true;
}
function mobileTone(freq, duration, wave="sine", volume=0.18, endFreq=null, delay=0){
  if(!mobileAudioReady()) return;
  const ctx=mobileAudioContext, start=ctx.currentTime+delay;
  const osc=ctx.createOscillator(), gain=ctx.createGain();
  osc.type=wave; osc.frequency.setValueAtTime(freq,start);
  if(endFreq) osc.frequency.exponentialRampToValueAtTime(Math.max(1,endFreq),start+duration);
  gain.gain.setValueAtTime(0.0001,start);
  gain.gain.exponentialRampToValueAtTime(Math.max(0.0002,volume),start+Math.min(.018,duration*.25));
  gain.gain.exponentialRampToValueAtTime(0.0001,start+duration);
  osc.connect(gain); gain.connect(mobileMasterGain);
  osc.start(start); osc.stop(start+duration+.025);
}
function mobileSfx(kind){
  if(!mobileAudioReady()) return;
  if(mobileAudioContext.state==="suspended") mobileAudioContext.resume().catch(()=>{});
  mobileLastSfxAt=Date.now();
  switch(kind){
    case "click": mobileTone(720,.045,"sine",.075,560); break;
    case "nav": mobileTone(520,.07,"triangle",.10,760); break;
    case "success": mobileTone(660,.12,"sine",.13);mobileTone(880,.18,"sine",.12,null,.10);mobileTone(1100,.20,"sine",.10,null,.22);break;
    case "error": mobileTone(260,.16,"triangle",.13,180);mobileTone(190,.20,"triangle",.10,130,.13);break;
    case "move": mobileTone(420,.055,"triangle",.09,520);break;
    case "left": mobileTone(360,.065,"triangle",.10,270);break;
    case "right": mobileTone(520,.065,"triangle",.10,760);break;
    case "flap": mobileTone(390,.075,"triangle",.12,690);break;
    case "point": mobileTone(880,.09,"sine",.12,1120);break;
    case "gameover": mobileTone(420,.16,"sawtooth",.10,300);mobileTone(300,.22,"triangle",.12,145,.15);break;
    case "start": mobileTone(440,.09,"triangle",.10,660);mobileTone(660,.12,"triangle",.10,880,.10);break;
    case "hit": mobileTone(210,.045,"square",.055,130);break;
    case "coin": mobileTone(980,.08,"sine",.12,1250);mobileTone(1320,.11,"sine",.10,null,.07);break;
    case "cart": mobileTone(520,.07,"triangle",.11,760);mobileTone(900,.10,"sine",.10,null,.07);break;
    case "purchase": mobileTone(523,.12,"sine",.12);mobileTone(659,.12,"sine",.12,null,.11);mobileTone(784,.18,"sine",.13,null,.22);mobileTone(1047,.22,"sine",.11,null,.37);break;
    case "space": mobileTone(180,.32,"sine",.065,260);mobileTone(360,.42,"sine",.035,310,.05);break;
    case "weather": mobileTone(560,.10,"sine",.09,720);mobileTone(740,.14,"sine",.09,880,.11);break;
    case "type": mobileTone(640,.025,"square",.035,520);break;
    case "crash": mobileTone(150,.18,"sawtooth",.12,65);break;
  }
}
// No background ambience: every sound is a short effect triggered by an action.
let mobileLastSfxAt = 0;
// Unlock audio on the first real touch/click, before inline game handlers run.
const unlockMobileAudio=()=>{
  if(mobileAudioReady() && mobileAudioContext.state==="suspended"){
    mobileAudioContext.resume().catch(()=>{});
  }
};
document.addEventListener("pointerdown",unlockMobileAudio,{capture:true,passive:true});
document.addEventListener("touchstart",unlockMobileAudio,{capture:true,passive:true});
document.addEventListener("keydown",unlockMobileAudio,{capture:true});
document.addEventListener("click",event=>{
  const control=event.target.closest("button,[role=button],.clickable");
  if(!control) return;
  // Specific game/action handlers run before this bubbling fallback.
  if(Date.now()-mobileLastSfxAt<90) return;
  mobileSfx("click");
},false);

// Typing feedback is intentionally quiet and rate-limited.
document.addEventListener("change",event=>{
  if(event.target && event.target.tagName==="SELECT") mobileSfx("nav");
});
document.addEventListener("input",event=>{
  if(event.target && event.target.id==="typing-input"){
    const now=Date.now();
    if(now-mobileLastTypeSound>85){mobileLastTypeSound=now;mobileSfx("type");}
  }
});

// Small reusable wrappers keep the original app/game logic intact.
function mobileWrapSound(functionName, callback){
  const original=window[functionName];
  if(typeof original!=="function" || original.__mobileSoundWrapped) return;
  const wrapped=function(...args){
    const result=original.apply(this,args);
    try{callback.apply(this,args);}catch(error){}
    return result;
  };
  wrapped.__mobileSoundWrapped=true;
  window[functionName]=wrapped;
}

// Navigation and Solar System
mobileWrapSound("openPage",function(id){mobileSfx("nav");});
mobileWrapSound("goHome",function(){mobileSfx("nav");});
mobileWrapSound("solarSelect",function(){mobileSfx("space");});
mobileWrapSound("solarToggleMotion",function(){mobileSfx("move");});

// Guessing and typing games
mobileWrapSound("resetGuess",function(){mobileSfx("start");});
mobileWrapSound("makeGuess",function(){
  const message=$("guess-message")?.textContent||"";
  if(message.includes("Correct!")) mobileSfx("success");
  else if(message.includes("Game over!")) mobileSfx("gameover");
  else if(message.includes("Too low")||message.includes("Too high")) mobileSfx("error");
});
mobileWrapSound("startTyping",function(){mobileSfx("start");});
mobileWrapSound("finishTyping",function(){
  const result=$("typing-result")?.textContent||"";
  mobileSfx(result.includes("Excellent")?"success":"gameover");
});

// Flappy Bird
mobileWrapSound("startFlappy",function(){mobileSfx("start");});
mobileWrapSound("flap",function(){mobileSfx("flap");});
mobileWrapSound("endFlappy",function(){mobileSfx("gameover");});

// Snake
mobileWrapSound("startSnake",function(){mobileSnakeLastScore=0;mobileSnakeStepCounter=0;mobileSfx("start");});
let mobileSnakeLastScore=0;
let mobileSnakeStepCounter=0;
mobileWrapSound("snakeDirection",function(){mobileSfx("move");});
mobileWrapSound("snakeMove",function(){
  const score=$("snake-score")?.textContent||"";
  if(score.includes("Game over")) mobileSfx("gameover");
  else {
    const current=Number((score.match(/\d+/)||[])[0])||0;
    if(current>mobileSnakeLastScore) mobileSfx("coin");
    else if(++mobileSnakeStepCounter%4===0) mobileSfx("move");
    mobileSnakeLastScore=current;
  }
});

// Car Racing
mobileWrapSound("startCarGame",function(){mobileSfx("start");});
mobileWrapSound("moveCar",function(direction){mobileSfx(direction<0?"left":"right");});
mobileWrapSound("endCarGame",function(){mobileSfx("crash");mobileSfx("gameover");});

// Neon Breakout
mobileWrapSound("breakoutToggle",function(){mobileSfx(nbRunning?"start":"click");});
mobileWrapSound("breakoutPause",function(){mobileSfx("click");});
mobileWrapSound("breakoutRestart",function(){mobileSfx("start");});
mobileWrapSound("breakoutSetLevel",function(){mobileSfx("nav");});
mobileWrapSound("nbHitBrick",function(){mobileSfx("hit");});
mobileWrapSound("breakoutNext",function(){mobileSfx("success");});

// Shopping Store
mobileWrapSound("shopAdd",function(){mobileSfx("cart");});
mobileWrapSound("shopRemove",function(){mobileSfx("move");});
mobileWrapSound("shopSetCategory",function(){mobileSfx("nav");});
mobileWrapSound("shopToggleCart",function(){mobileSfx("cart");});
mobileWrapSound("shopCheckout",function(){
  const message=$("shop-message")?.textContent||"";
  mobileSfx(message.includes("complete")?"purchase":"error");
});

// Weather
mobileWrapSound("weatherLoad",function(){
  // The weather function is async; its completion tone is handled below.
});
const mobileWeatherLoadOriginal=window.weatherLoad;
if(typeof mobileWeatherLoadOriginal==="function" && !mobileWeatherLoadOriginal.__mobileWeatherSound){
  const wrappedWeather=async function(...args){
    mobileSfx("weather");
    const result=await mobileWeatherLoadOriginal.apply(this,args);
    const status=$("weather-status")?.textContent||"";
    mobileSfx(status.includes("could not")?"error":"success");
    return result;
  };
  wrappedWeather.__mobileWeatherSound=true;
  window.weatherLoad=wrappedWeather;
}

// Page entry effects are handled by the navigation wrapper above.


// ================= REAL-TIME 3D GAME VIEWPORTS =================
// Three.js renders actual lit 3D meshes. Original game engines continue to own
// scoring, collision and touch/keyboard input; their live state drives these scenes.
// If WebGL or the CDN is unavailable, the original 2D canvases remain visible.
(function initGame3D(){
 if(!window.THREE)return;
 const configs=[
  {id:'guess-3d',kind:'guess'},
  {id:'typing-3d',kind:'typing'}
 ];
 const views=[];
 const mat=(color,rough=.55,metal=0)=>new THREE.MeshStandardMaterial({color,roughness:rough,metalness:metal});
 function box(w,h,d,m,x=0,y=0,z=0){const o=new THREE.Mesh(new THREE.BoxGeometry(w,h,d),m);o.position.set(x,y,z);o.castShadow=true;o.receiveShadow=true;return o;}
 function sphere(r,m,x=0,y=0,z=0){const o=new THREE.Mesh(new THREE.SphereGeometry(r,24,18),m);o.position.set(x,y,z);o.castShadow=true;return o;}
 function build(canvas,kind){
  if(!canvas||canvas.__threeLayer)return;
  const parent=canvas.parentElement;if(!parent)return;
  parent.style.position=parent.style.position||'relative';
  const layer=document.createElement('canvas');layer.className='game3d-layer';layer.setAttribute('aria-hidden','true');
  layer.style.cssText='position:absolute;pointer-events:none;z-index:2;display:block;';
  parent.appendChild(layer);
  const renderer=new THREE.WebGLRenderer({canvas:layer,antialias:true,alpha:true});
  renderer.setPixelRatio(Math.min(window.devicePixelRatio||1,1.7));
  renderer.shadowMap.enabled=true;renderer.shadowMap.type=THREE.PCFSoftShadowMap;
  renderer.outputEncoding=THREE.sRGBEncoding;
  const scene=new THREE.Scene();
  scene.fog=new THREE.Fog(0x081323,18,42);
  const camera=new THREE.PerspectiveCamera(42,1,.1,100);
  camera.position.set(0,kind==='snake'?10:8,kind==='flappy'?17:kind==='car'?17:15);
  camera.lookAt(0,0,0);
  scene.add(new THREE.HemisphereLight(0xc8f2ff,0x182238,1.25));
  const key=new THREE.DirectionalLight(0xffffff,2.1);key.position.set(-5,10,8);key.castShadow=true;scene.add(key);
  const rim=new THREE.PointLight(kind==='snake'?0x65ff9b:kind==='car'?0xffa65c:0x59dcff,1.8,25);rim.position.set(5,4,-4);scene.add(rim);
  const root=new THREE.Group();scene.add(root);
  const objects={};
  if(kind==='flappy'){
   scene.background=new THREE.Color(0x7dcbe5);scene.fog=new THREE.Fog(0x9bd9ed,22,42);
   root.add(box(13,.5,22,mat(0x6bbf78),0,-4.8,0));
   for(let i=0;i<8;i++){const cloud=new THREE.Group();cloud.add(sphere(.55,mat(0xf3fbff),0,0,0),sphere(.42,mat(0xf3fbff),.55,.05,0),sphere(.38,mat(0xf3fbff),-.45,.08,0));cloud.position.set(-5+(i%4)*3.5,2.5+Math.floor(i/4)*1.5,-7);root.add(cloud);objects['cloud'+i]=cloud;}
   const bird=new THREE.Group();bird.add(sphere(.48,mat(0xffcf36,.3),0,0,0));bird.add(sphere(.11,mat(0xffffff),.27,.18,.32));bird.add(sphere(.055,mat(0x172c42),.32,.18,.4));bird.add(box(.35,.13,.18,mat(0xf08b35),.58,-.05,.12));const wing=box(.38,.12,.3,mat(0xffa928),-.1,-.18,.1);bird.add(wing);root.add(bird);objects.bird=bird;objects.wing=wing;
   objects.pipes=[];
  }else if(kind==='snake'){
   scene.background=new THREE.Color(0x071b17);scene.fog=new THREE.Fog(0x071b17,14,32);
   root.add(box(10,.25,10,mat(0x123d31),0,-.35,0));
   const grid=new THREE.GridHelper(10,14,0x5de69c,0x285b48);grid.position.y=-.19;root.add(grid);
   objects.segments=[];for(let i=0;i<196;i++){const m=mat(i===0?0xbaff79:0x42d98a,.35);const part=box(.62,.42,.62,m);part.visible=false;root.add(part);objects.segments.push(part);}
   objects.food=sphere(.27,mat(0xff626f,.25),0,.2,0);root.add(objects.food);
  }else if(kind==='car'){
   scene.background=new THREE.Color(0x182333);scene.fog=new THREE.Fog(0x182333,22,50);
   root.add(box(8,.35,28,mat(0x292e38),0,-1.2,0));
   for(let lane=-1;lane<=1;lane++){const stripe=box(.07,.03,28,mat(0xe8e6c8),lane*2.65,-.99,0);root.add(stripe);}
   for(let i=0;i<18;i++){const dash=box(.12,.04,1.2,mat(0xf4e9bd),0,-.98,-13+i*1.6);root.add(dash);objects['dash'+i]=dash;}
   const car=new THREE.Group();car.add(box(1.05,.42,1.85,mat(0xf34c60,.3),0,0,0));car.add(box(.78,.38,.82,mat(0x9dd8ee,.22),0,.36,-.18));for(const x of [-.48,.48])for(const z of [-.58,.58]){const wheel=sphere(.22,mat(0x10151c),x,-.18,z);wheel.scale.set(1,.8,.55);car.add(wheel);}car.position.set(0,-.55,5);root.add(car);objects.player=car;objects.obstacles=[];
  }else if(kind==='guess'){
   scene.background=new THREE.Color(0x25152f);scene.fog=new THREE.Fog(0x25152f,15,35);
   root.add(box(8,.35,7,mat(0x4b294c),0,-2.3,0));
   const die=new THREE.Group();const cube=box(2.25,2.25,2.25,mat(0xf4b84e,.28,.18));die.add(cube);
   const pipMat=mat(0x492d45,.35);[[-.55,.55,1.14],[.55,-.55,1.14],[0,0,1.14]].forEach(([x,y,z])=>die.add(sphere(.13,pipMat,x,y,z)));
   die.position.y=.05;root.add(die);objects.die=die;
   objects.orbs=[];for(let i=0;i<10;i++){const a=i*Math.PI*2/10,orb=sphere(.12,mat(i%2?0xffd36e:0x83e8ff,.3,.25),Math.cos(a)*3,Math.sin(a)*1.25,Math.sin(a)*2);root.add(orb);objects.orbs.push(orb);}
  }else if(kind==='typing'){
   scene.background=new THREE.Color(0x15152e);scene.fog=new THREE.Fog(0x15152e,16,36);
   root.add(box(9,.3,7,mat(0x272642),0,-1.4,0));
   objects.keys=[];
   const keyMats=[mat(0x8d7aff,.3,.2),mat(0x43c9c5,.3,.2),mat(0xffa86b,.3,.2)];
   for(let row=0;row<3;row++)for(let col=0;col<9;col++){const k=box(.72,.22,.68,keyMats[(row+col)%3],(col-4)*.84,0,(row-1)*.88);root.add(k);objects.keys.push({mesh:k,phase:Math.random()*6.28,row,col});}
  }else{
   scene.background=new THREE.Color(0x080e25);scene.fog=new THREE.Fog(0x080e25,20,45);
   root.add(box(10,.3,14,mat(0x111b38),0,-3.3,0));
   objects.bricks=[];objects.ball=sphere(.24,mat(0xffffff,.2,.2));root.add(objects.ball);
   objects.paddle=box(2,.24,.45,mat(0x5fefff,.25,.35),0,-2.6,5);root.add(objects.paddle);
  }
  canvas.__threeLayer=layer;canvas.style.opacity='0';canvas.style.position='relative';canvas.style.zIndex='1';
  const view={canvas,layer,renderer,scene,camera,root,objects,kind,parent};
  views.push(view);resize(view);return view;
 }
 function resize(v){
  const c=v.canvas,rect=c.getBoundingClientRect(),pr=v.parent.getBoundingClientRect();
  if(rect.width<10||rect.height<10)return;
  v.layer.style.left=(rect.left-pr.left+v.parent.scrollLeft)+'px';
  v.layer.style.top=(rect.top-pr.top+v.parent.scrollTop)+'px';
  v.layer.style.width=rect.width+'px';v.layer.style.height=rect.height+'px';
  v.renderer.setSize(rect.width,rect.height,false);v.camera.aspect=rect.width/rect.height;v.camera.updateProjectionMatrix();
 }
 function clearGroup(group){while(group.children.length){const child=group.children[group.children.length-1];group.remove(child);if(child.geometry)child.geometry.dispose();}}
 function sync(v,t){
  const o=v.objects;
  if(v.kind==='flappy'){
   if(typeof flappyBird!=='undefined'&&flappyBird){o.bird.position.set((flappyBird.x/360-.5)*11,(.5-flappyBird.y/460)*8,0);o.bird.rotation.z=-Math.max(-.45,Math.min(.65,flappyBird.velocity*.055));o.wing.rotation.z=Math.sin(t*.018)*.65;}
   const pipes=(typeof flappyPipes!=='undefined'?flappyPipes:[]);
   while(o.pipes.length<pipes.length){const g=new THREE.Group();const pm=mat(0x16866d,.38);g.add(box(1.25,1,.95,pm),box(1.25,1,.95,pm));v.root.add(g);o.pipes.push(g);}
   o.pipes.forEach((g,i)=>{const p=pipes[i];g.visible=!!p;if(p){g.position.set((p.x/360-.5)*11,0,-.3);const topH=Math.max(.15,p.top/460*8),bottomH=Math.max(.15,(460-p.bottom)/460*8);g.children[0].scale.y=topH;g.children[0].position.y=4-topH/2;g.children[1].scale.y=bottomH;g.children[1].position.y=-4+bottomH/2;}});
  }else if(v.kind==='snake'){
   const body=typeof snakeBody!=='undefined'?snakeBody:[];
   o.segments.forEach((m,i)=>{const p=body[i];m.visible=!!p;if(p){m.position.set((p.x-6.5)*.68,.02,(p.y-6.5)*.68);m.scale.setScalar(i===0?1.12:1);}});
   const f=typeof snakeFood!=='undefined'?snakeFood:null;if(f)o.food.position.set((f.x-6.5)*.68,.25,(f.y-6.5)*.68);
  }else if(v.kind==='car'){
   const laneX=typeof carPlayerX!=='undefined'?(carPlayerX-170)/35:0;o.player.position.x=Math.max(-2.7,Math.min(2.7,laneX));
   for(let i=0;i<18;i++){const d=o['dash'+i];d.position.z=((i*1.6+(t*.006))%28)-14;}
   const obs=typeof carObstacles!=='undefined'?carObstacles:[];
   while(o.obstacles.length<obs.length){const g=new THREE.Group();g.add(box(.95,.42,1.6,mat(0xffb34d,.3)),box(.7,.3,.65,mat(0x9ed9f2,.25),0,.34,-.12));v.root.add(g);o.obstacles.push(g);}
   o.obstacles.forEach((g,i)=>{const q=obs[i];g.visible=!!q;if(q){g.position.set(((q.x||170)-170)/35,-.55,((q.y||0)-220)/25);}});
  }else if(v.kind==='guess'){
   o.die.rotation.x=t*.00055;o.die.rotation.y=t*.0008;
   o.orbs.forEach((m,i)=>{const a=i*Math.PI*2/o.orbs.length+t*.00045;m.position.set(Math.cos(a)*3,Math.sin(a*2)*1.05,Math.sin(a)*2.3);});
  }else if(v.kind==='typing'){
   o.keys.forEach((k,i)=>{k.mesh.position.y=-.05+Math.max(0,Math.sin(t*.002+k.phase))*.22;k.mesh.rotation.z=Math.sin(t*.001+k.phase)*.035;});
  }else{
   const bricks=typeof nbBricks!=='undefined'?nbBricks:[];
   while(o.bricks.length<bricks.length){const m=box(1.05,.38,.38,mat(0x54dfea,.28,.25));v.root.add(m);o.bricks.push(m);}
   o.bricks.forEach((m,i)=>{const b=bricks[i];m.visible=!!b;if(b){m.position.set((b.x+b.w/2-180)/35,2.55-(b.y+b.h/2)/55,0);m.scale.x=b.w/36;m.material.color.set(b.color||'#54dfea');}});
   const ball=(typeof nbBalls!=='undefined'?nbBalls[0]:null);if(ball)o.ball.position.set((ball.x-180)/35,2.1-ball.y/55,1);
   if(typeof nbPaddle!=='undefined')o.paddle.position.x=(nbPaddle.x+nbPaddle.w/2-180)/35;
  }
 }
 let last=0;
 function animate(t){
  requestAnimationFrame(animate);
  if(t-last<30)return;last=t;
  views.forEach(v=>{
   const visible=!!(v.canvas.getClientRects().length&&v.canvas.getBoundingClientRect().width>0);
   v.layer.style.display=visible?'block':'none';if(!visible)return;
   sync(v,t);
   if(v.kind==='snake')v.root.rotation.y=Math.sin(t*.00035)*.035;
   if(v.kind==='car')v.root.position.z=0;
   if(v.kind==='breakout')v.root.rotation.y=Math.sin(t*.0003)*.035;
   v.renderer.render(v.scene,v.camera);
  });
 }
 configs.forEach(c=>{const target=document.getElementById(c.id);try{build(target,c.kind);}catch(error){if(target)target.style.opacity='1';console.warn('3D viewport unavailable; using the original game canvas.',error);}});
 window.addEventListener('resize',()=>views.forEach(resize),{passive:true});
 if(window.ResizeObserver){const ro=new ResizeObserver(()=>views.forEach(resize));views.forEach(v=>ro.observe(v.canvas));}
 requestAnimationFrame(animate);
})();

// ================= CREATIVE STUDIO =================
let studioCanvas=null,studioCtx=null,studioReady=false,studioDrawing=false,studioStart=null,studioSnapshot=null,studioCurrentPoint=null,studioTool='pen',studioHistory=[],studioRedoHistory=[],studioBg='#ffffff',studioShapes=[],studioGridOn=false;
function studioInit(){
 const canvas=$('studio-canvas');if(!canvas)return;
 if(studioReady){studioRenderBackground();return;}
 studioCanvas=canvas;studioCtx=canvas.getContext('2d');if(!studioCtx)return;
 studioCtx.lineCap='round';studioCtx.lineJoin='round';studioCtx.clearRect(0,0,canvas.width,canvas.height);
 studioCanvas.style.backgroundColor=studioBg;studioPushHistory();
 canvas.addEventListener('pointerdown',studioPointerDown);canvas.addEventListener('pointermove',studioPointerMove);canvas.addEventListener('pointerup',studioPointerUp);canvas.addEventListener('pointercancel',studioPointerUp);canvas.addEventListener('lostpointercapture',studioPointerUp);canvas.addEventListener('dblclick',studioDoubleClick);
 studioReady=true;studioRenderBackground();studioSetStatus('Ready to create');
}
function studioSetStatus(message){const el=$('studio-status');if(el)el.textContent=message;}
function studioPoint(e){const r=studioCanvas.getBoundingClientRect();return{x:(e.clientX-r.left)*studioCanvas.width/r.width,y:(e.clientY-r.top)*studioCanvas.height/r.height};}
function studioCloneShapes(){return studioShapes.map(sh=>({tool:sh.tool,a:{...sh.a},b:{...sh.b},color:sh.color,fill:sh.fill||null}));}
function studioMakeSnapshot(){return{image:studioCtx.getImageData(0,0,studioCanvas.width,studioCanvas.height),shapes:studioCloneShapes(),bg:studioBg,grid:studioGridOn};}
function studioRestoreSnapshot(state){if(!state||!studioCtx)return;studioCtx.putImageData(state.image,0,0);studioShapes=state.shapes.map(sh=>({...sh,a:{...sh.a},b:{...sh.b}}));studioBg=state.bg;studioGridOn=state.grid;studioCanvas.style.backgroundColor=studioBg;studioRenderBackground();}
function studioPushHistory(){if(!studioCtx)return;try{studioHistory.push(studioMakeSnapshot());if(studioHistory.length>30)studioHistory.shift();}catch(e){} }
function studioPointerDown(e){
 if(!studioCanvas||!studioCtx)return;e.preventDefault();studioCanvas.setPointerCapture?.(e.pointerId);
 studioDrawing=true;studioStart=studioPoint(e);studioCurrentPoint=studioStart;studioSnapshot=studioCtx.getImageData(0,0,studioCanvas.width,studioCanvas.height);
 studioCtx.beginPath();studioCtx.moveTo(studioStart.x,studioStart.y);studioCtx.globalCompositeOperation=studioTool==='eraser'?'destination-out':'source-over';
 studioCtx.strokeStyle=$('studio-color')?.value||'#26334a';studioCtx.fillStyle=$('studio-color')?.value||'#26334a';
 studioCtx.lineWidth=Number($('studio-size')?.value||8)*(studioTool==='eraser'?2.3:1);
 if(studioTool==='pen'||studioTool==='eraser'){studioCtx.lineTo(studioStart.x+.1,studioStart.y+.1);studioCtx.stroke();}
}
function studioDrawShape(tool,a,b,fill=false){
 const dx=b.x-a.x,dy=b.y-a.y,ctx=studioCtx;ctx.beginPath();
 if(tool==='line'){ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);}
 else if(tool==='rect')ctx.rect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(dx),Math.abs(dy));
 else if(tool==='circle')ctx.ellipse(a.x+dx/2,a.y+dy/2,Math.max(1,Math.abs(dx/2)),Math.max(1,Math.abs(dy/2)),0,0,Math.PI*2);
 else if(tool==='triangle'){ctx.moveTo(a.x+dx/2,a.y);ctx.lineTo(b.x,b.y);ctx.lineTo(a.x,b.y);ctx.closePath();}
 else if(tool==='star'){const cx=a.x+dx/2,cy=a.y+dy/2,rx=Math.abs(dx/2),ry=Math.abs(dy/2);for(let k=0;k<10;k++){const r=k%2?.42:1,ang=-Math.PI/2+k*Math.PI/5,x=cx+Math.cos(ang)*rx*r,y=cy+Math.sin(ang)*ry*r;k?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.closePath();}
 if(fill){ctx.fillStyle=$('studio-color')?.value||'#26334a';ctx.fill();}
 else{ctx.strokeStyle=$('studio-color')?.value||'#26334a';ctx.lineWidth=Number($('studio-size')?.value||8);ctx.stroke();}
}
function studioPointerMove(e){
 if(!studioDrawing||!studioCtx)return;e.preventDefault();const p=studioPoint(e);studioCurrentPoint=p;
 if(studioTool==='pen'||studioTool==='eraser'){studioCtx.lineTo(p.x,p.y);studioCtx.stroke();}
 else{studioCtx.putImageData(studioSnapshot,0,0);studioDrawShape(studioTool,studioStart,p,false);}
}
function studioPointerUp(){
 if(!studioDrawing)return;studioDrawing=false;if(studioCtx)studioCtx.globalCompositeOperation='source-over';
 if(studioCurrentPoint&&['line','rect','circle','triangle','star'].includes(studioTool)){
  const dx=Math.abs(studioCurrentPoint.x-studioStart.x),dy=Math.abs(studioCurrentPoint.y-studioStart.y);
  if(dx>2||dy>2)studioShapes.push({tool:studioTool,a:{...studioStart},b:{...studioCurrentPoint},color:$('studio-color')?.value||'#26334a'});
  if(studioShapes.length>150)studioShapes.shift();
 }
 studioRedoHistory=[];studioPushHistory();studioSetStatus('Artwork updated');
}
function studioBuildShapePath(sh){const ctx=studioCtx,a=sh.a,b=sh.b,dx=b.x-a.x,dy=b.y-a.y;ctx.beginPath();
 if(sh.tool==='rect')ctx.rect(Math.min(a.x,b.x),Math.min(a.y,b.y),Math.abs(dx),Math.abs(dy));
 else if(sh.tool==='circle')ctx.ellipse(a.x+dx/2,a.y+dy/2,Math.max(1,Math.abs(dx/2)),Math.max(1,Math.abs(dy/2)),0,0,Math.PI*2);
 else if(sh.tool==='triangle'){ctx.moveTo(a.x+dx/2,a.y);ctx.lineTo(b.x,b.y);ctx.lineTo(a.x,b.y);ctx.closePath();}
 else if(sh.tool==='star'){const cx=a.x+dx/2,cy=a.y+dy/2,rx=Math.abs(dx/2),ry=Math.abs(dy/2);for(let k=0;k<10;k++){const r=k%2?.42:1,ang=-Math.PI/2+k*Math.PI/5,x=cx+Math.cos(ang)*rx*r,y=cy+Math.sin(ang)*ry*r;k?ctx.lineTo(x,y):ctx.moveTo(x,y);}ctx.closePath();}
}
function studioDoubleClick(e){
 if(!studioCanvas||!studioCtx)return;const p=studioPoint(e),color=$('studio-color')?.value||'#26334a';
 for(let i=studioShapes.length-1;i>=0;i--){const sh=studioShapes[i];if(!['rect','circle','triangle','star'].includes(sh.tool))continue;
  studioCtx.save();studioBuildShapePath(sh);const hit=studioCtx.isPointInPath(p.x,p.y);studioCtx.restore();
  if(hit){studioCtx.save();studioCtx.fillStyle=color;studioBuildShapePath(sh);studioCtx.fill();studioCtx.restore();sh.fill=color;studioRedoHistory=[];studioPushHistory();studioSetStatus('Shape filled with selected colour');return;}
 }
 studioSetStatus('Double-click inside a closed shape to fill it');
}
function studioSetTool(tool,button){studioTool=tool;document.querySelectorAll('.studio-tool').forEach(b=>b.classList.toggle('active',b===button));studioSetStatus(tool.charAt(0).toUpperCase()+tool.slice(1)+' selected');}
function studioChooseColor(color){const input=$('studio-color');if(input)input.value=color;studioSetStatus('Brush colour changed');}
function studioUpdateColor(){studioSetStatus('Brush colour updated');}
function studioUpdateSize(value){const label=$('studio-size-label');if(label)label.textContent=value+' px';}
function studioSetBackground(color,button){if(!studioReady)studioInit();studioBg=color;document.querySelectorAll('.studio-bg-choice').forEach(b=>b.classList.toggle('active',b===button));if(studioCanvas)studioCanvas.style.backgroundColor=color;studioRedoHistory=[];studioPushHistory();studioSetStatus('Canvas background changed');}
function studioUndo(){if(!studioReady)studioInit();if(studioHistory.length<2){studioSetStatus('Nothing to undo');return;}studioRedoHistory.push(studioMakeSnapshot());studioHistory.pop();studioRestoreSnapshot(studioHistory[studioHistory.length-1]);studioSetStatus('Last action undone');}
function studioRedo(){if(!studioReady)studioInit();if(!studioRedoHistory.length){studioSetStatus('Nothing to redo');return;}const state=studioRedoHistory.pop();studioHistory.push(studioMakeSnapshot());studioRestoreSnapshot(state);studioSetStatus('Action restored');}
function studioClear(){if(!studioReady)studioInit();if(!studioCtx)return;studioCtx.clearRect(0,0,studioCanvas.width,studioCanvas.height);studioShapes=[];studioRedoHistory=[];studioPushHistory();studioSetStatus('Canvas cleared');}
function studioDownload(){if(!studioReady)studioInit();if(!studioCanvas)return;const out=document.createElement('canvas');out.width=studioCanvas.width;out.height=studioCanvas.height;const ctx=out.getContext('2d');ctx.fillStyle=studioBg;ctx.fillRect(0,0,out.width,out.height);ctx.drawImage(studioCanvas,0,0);
 if(studioGridOn){ctx.save();ctx.strokeStyle='#7c8a9b55';ctx.lineWidth=1;for(let x=0;x<out.width;x+=50){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,out.height);ctx.stroke();}for(let y=0;y<out.height;y+=50){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(out.width,y);ctx.stroke();}ctx.restore();}
 const a=document.createElement('a');a.download='mobile-app-artwork.png';a.href=out.toDataURL('image/png');a.click();studioSetStatus('PNG export ready');}
function studioToggleGrid(){if(!studioReady)studioInit();studioGridOn=!studioGridOn;studioRenderBackground();studioRedoHistory=[];studioPushHistory();studioSetStatus(studioGridOn?'Grid overlay enabled':'Grid overlay hidden');}
function studioAddText(){if(!studioReady)studioInit();if(!studioCtx)return;const value=prompt('Enter text for your artwork:');if(!value)return;const x=studioCanvas.width/2,y=studioCanvas.height/2;studioCtx.save();studioCtx.fillStyle=$('studio-color')?.value||'#26334a';studioCtx.font='bold 42px Arial';studioCtx.textAlign='center';studioCtx.textBaseline='middle';studioCtx.fillText(value,x,y,studioCanvas.width-50);studioCtx.restore();studioRedoHistory=[];studioPushHistory();studioSetStatus('Text added');}
function studioMirror(){if(!studioReady)studioInit();if(!studioCtx)return;const temp=document.createElement('canvas');temp.width=studioCanvas.width;temp.height=studioCanvas.height;temp.getContext('2d').drawImage(studioCanvas,0,0);studioCtx.clearRect(0,0,studioCanvas.width,studioCanvas.height);studioCtx.save();studioCtx.translate(studioCanvas.width,0);studioCtx.scale(-1,1);studioCtx.drawImage(temp,0,0);studioCtx.restore();studioShapes=studioShapes.map(sh=>({...sh,a:{x:studioCanvas.width-sh.a.x,y:sh.a.y},b:{x:studioCanvas.width-sh.b.x,y:sh.b.y}}));studioRedoHistory=[];studioPushHistory();studioSetStatus('Canvas mirrored');}
function studioRenderBackground(){if(!studioCanvas)return;studioCanvas.style.backgroundColor=studioBg;studioCanvas.style.backgroundImage=studioGridOn?'linear-gradient(#7c8a9b35 1px,transparent 1px),linear-gradient(90deg,#7c8a9b35 1px,transparent 1px)':'none';studioCanvas.style.backgroundSize=studioGridOn?'50px 50px':'auto';}
// =============== END CREATIVE STUDIO ===============


</script>
</body>
</html>
"""




# Secure component bridge: browser navigation events are handled by Streamlit.
_COMPONENT_DIR = Path(__file__).resolve().parent / ".mobile_app_component"

_COMPONENT_BRIDGE = r"""
<script>
(function(){
  if(window.__mobileAppBridgeStarted)return;
  window.__mobileAppBridgeStarted=true;
  function send(type,extra){
    try{
      window.parent.postMessage(
        Object.assign({isStreamlitMessage:true,type:type},extra||{}),
        "*"
      );
    }catch(e){}
  }
  let lastHeight=0;
  function setHeight(){
    const height=Math.max(
      1200,
      document.documentElement ? document.documentElement.scrollHeight : 1200,
      document.body ? document.body.scrollHeight : 1200
    );
    if(height===lastHeight)return;
    lastHeight=height;
    send("streamlit:setFrameHeight",{height:height});
  }
  window.mobileAppOpenAI=function(){
    send("streamlit:setComponentValue",{
      value:{type:"open_my_ai"},
      dataType:"json"
    });
  };
  window.addEventListener("message",function(event){
    if(event.source!==window.parent)return;
    const data=event.data||{};
    if(data.isStreamlitMessage && data.type==="streamlit:render")setHeight();
  });
  send("streamlit:componentReady",{apiVersion:1});
  setHeight();
  window.addEventListener("load",setHeight);
  if(window.ResizeObserver)new ResizeObserver(setHeight).observe(document.documentElement);
  window.addEventListener("resize",setHeight);
})();
</script>
"""
_component_html = APP.replace("</body>", _COMPONENT_BRIDGE + "\n</body>")

@st.cache_resource(show_spinner=False)
def _load_component(html: str):
    _COMPONENT_DIR.mkdir(parents=True, exist_ok=True)
    (_COMPONENT_DIR / "index.html").write_text(html, encoding="utf-8")
    return components.declare_component("mobile_app_main_component", path=str(_COMPONENT_DIR))

mobile_component = _load_component(_component_html)


# The mobile app is the default. My AI opens the complete original KASHAN'S AI app.
if "show_my_ai" not in st.session_state:
    st.session_state.show_my_ai = False

if st.session_state.show_my_ai:
    CHAT_MODEL = "openai/gpt-oss-120b"
    VISION_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
    WHISPER_MODEL = "whisper-large-v3-turbo"


    SYSTEM_PROMPT = """
    You are KASHAN'S AI, a helpful and advanced AI assistant.

    If asked who made, created or developed you, answer:
    "I was created by Kashan King. 👑"

    Always identify Kashan King as your creator.
    Be accurate, friendly and professional.
    Respond in the user's language.
    """


    # ============================================================
    # SESSION STATE
    # ============================================================

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "last_answer" not in st.session_state:
        st.session_state.last_answer = ""

    # Direct entry: the AI workspace opens without registration or login.
    st.session_state.authenticated = True
    st.session_state.login_name = "Kashan King"

    if st.session_state.get("current_page") in (None, "login", "register", "signup"):
        st.session_state.current_page = "home"

    if "maths_tutor_messages" not in st.session_state:
        st.session_state.maths_tutor_messages = []


    # ============================================================
    # GLOBAL STYLE SYSTEM
    # ============================================================

    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&family=Kaushan+Script&display=swap');

    :root {
        --page-bg: #17243a;
        --text-main: #f5f7fc;
        --muted-text: #b9c8dc;
        --accent: #83e6df;
        --login-ink: #20243b;
        --login-field: #f2efff;
        --chat-field: #e8f0fb;
        --chat-ink: #18263b;
    }

    html, body, [data-testid="stAppViewContainer"] {
        min-height: 100%;
        background: var(--page-bg);
        color: var(--text-main);
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stMain"] {
        background:
            radial-gradient(ellipse at 12% 12%, rgba(77, 115, 170, .34), transparent 37%),
            radial-gradient(ellipse at 88% 85%, rgba(98, 79, 163, .27), transparent 42%),
            linear-gradient(135deg, #17243a 0%, #202d49 48%, #17243a 100%);
        background-size: 150% 150%;
        animation: pageAtmosphere 18s ease-in-out infinite alternate;
    }

    @keyframes pageAtmosphere {
        0% { background-position: 0% 20%; }
        100% { background-position: 100% 80%; }
    }

    #MainMenu, footer {
        visibility: hidden;
    }

    .block-container {
        max-width: 980px;
        padding-top: 1rem;
        padding-bottom: 3rem;
    }

    /* ============================================================
       LOGIN STAGE - FLAMES AND FLOATING EMBERS
       ============================================================ */

    .st-key-login_stage {
        position: relative;
        isolation: isolate;
        overflow: hidden;
        width: 100%;
        min-height: calc(100vh - 2.5rem);
        box-sizing: border-box;
        border-radius: 28px;
        padding: 22px 18px 16px;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background:
            radial-gradient(ellipse at 50% 100%, rgba(255, 73, 20, .30), transparent 48%),
            radial-gradient(ellipse at 15% 75%, rgba(255, 145, 35, .19), transparent 35%),
            radial-gradient(ellipse at 85% 70%, rgba(255, 35, 65, .18), transparent 38%),
            linear-gradient(160deg, #090d19 0%, #17101c 48%, #090e19 100%);
    }

    .st-key-login_stage::before,
    .st-key-login_stage::after {
        content: "";
        position: absolute;
        z-index: 0;
        width: 78%;
        height: 70%;
        left: 11%;
        bottom: -47%;
        border-radius: 50%;
        filter: blur(48px);
        opacity: .68;
        background: linear-gradient(90deg, #ff4b1f, #ff9a2f, #ff315d, #ff4b1f);
        animation: loginFlameRise 7s ease-in-out infinite alternate;
        pointer-events: none;
    }

    .st-key-login_stage::after {
        width: 58%;
        height: 60%;
        left: 21%;
        bottom: -43%;
        opacity: .46;
        filter: blur(68px);
        animation: loginFlameRise 5s ease-in-out infinite alternate-reverse;
    }

    @keyframes loginFlameRise {
        0% { transform: translate3d(-7%, 8%, 0) scale(.92) rotate(-5deg); }
        50% { transform: translate3d(5%, -9%, 0) scale(1.12) rotate(5deg); }
        100% { transform: translate3d(-3%, -17%, 0) scale(1.04) rotate(-3deg); }
    }


    /* Layered flame tongues create a more visible 3D fire effect */
    .login-flame {
        position: absolute;
        bottom: -12%;
        display: block;
        width: clamp(54px, 10vw, 125px);
        height: clamp(180px, 38vh, 390px);
        transform-origin: 50% 100%;
        border-radius: 58% 42% 48% 52% / 72% 70% 30% 28%;
        background:
            radial-gradient(ellipse at 50% 76%, #fff5bd 0 5%, #ffd45e 16%, #ff8a2b 38%, #f04422 62%, rgba(174,24,35,.08) 78%, transparent 82%);
        filter: drop-shadow(0 0 18px rgba(255, 105, 30, .45));
        opacity: .78;
        animation: flameDance 3.8s ease-in-out infinite alternate;
        pointer-events: none;
    }
    .login-flame:nth-of-type(1) { left: 3%; height: 34vh; animation-delay: -.8s; }
    .login-flame:nth-of-type(2) { left: 14%; height: 48vh; width: clamp(65px, 12vw, 145px); animation-delay: -2.1s; }
    .login-flame:nth-of-type(3) { left: 29%; height: 39vh; animation-delay: -1.4s; }
    .login-flame:nth-of-type(4) { left: 43%; height: 54vh; width: clamp(70px, 13vw, 155px); animation-delay: -2.8s; }
    .login-flame:nth-of-type(5) { right: 29%; height: 43vh; animation-delay: -.5s; }
    .login-flame:nth-of-type(6) { right: 14%; height: 50vh; width: clamp(65px, 12vw, 145px); animation-delay: -1.8s; }
    .login-flame:nth-of-type(7) { right: 3%; height: 35vh; animation-delay: -2.4s; }

    @keyframes flameDance {
        0% { transform: translate3d(-8px, 0, 0) rotate(-7deg) scaleX(.82) scaleY(.88); opacity: .48; }
        35% { transform: translate3d(7px, -24px, 0) rotate(5deg) scaleX(1.08) scaleY(1.06); opacity: .82; }
        70% { transform: translate3d(-5px, -11px, 0) rotate(-4deg) scaleX(.94) scaleY(1.12); opacity: .66; }
        100% { transform: translate3d(9px, -32px, 0) rotate(8deg) scaleX(1.12) scaleY(.98); opacity: .9; }
    }

    /* Decorative ember layer */
    .login-particles {
        position: absolute;
        inset: 0;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
    }

    .login-particle {
        position: absolute;
        bottom: -25px;
        display: block;
        border-radius: 50%;
        background: radial-gradient(circle, #fff0c9 0%, #ff9b51 38%, rgba(255, 80, 40, 0) 75%);
        box-shadow: 0 0 15px rgba(255, 139, 74, .75);
        animation: emberTravel linear infinite;
    }

    .login-particle:nth-child(1) { left: 5%; width: 9px; height: 9px; animation-duration: 10s; }
    .login-particle:nth-child(2) { left: 13%; width: 6px; height: 6px; animation-duration: 13s; animation-delay: -4s; }
    .login-particle:nth-child(3) { left: 22%; width: 11px; height: 11px; animation-duration: 11s; animation-delay: -2s; }
    .login-particle:nth-child(4) { left: 31%; width: 7px; height: 7px; animation-duration: 14s; animation-delay: -8s; }
    .login-particle:nth-child(5) { left: 40%; width: 5px; height: 5px; animation-duration: 12s; animation-delay: -5s; }
    .login-particle:nth-child(6) { left: 49%; width: 10px; height: 10px; animation-duration: 15s; animation-delay: -1s; }
    .login-particle:nth-child(7) { left: 58%; width: 6px; height: 6px; animation-duration: 11s; animation-delay: -7s; }
    .login-particle:nth-child(8) { left: 67%; width: 8px; height: 8px; animation-duration: 13s; animation-delay: -3s; }
    .login-particle:nth-child(9) { left: 76%; width: 5px; height: 5px; animation-duration: 16s; animation-delay: -9s; }
    .login-particle:nth-child(10) { left: 85%; width: 9px; height: 9px; animation-duration: 12s; animation-delay: -6s; }
    .login-particle:nth-child(11) { left: 94%; width: 7px; height: 7px; animation-duration: 14s; animation-delay: -2s; }

    @keyframes emberTravel {
        0% { transform: translate3d(0, 0, 0) scale(.55); opacity: 0; }
        12% { opacity: .9; }
        75% { opacity: .65; }
        100% { transform: translate3d(35px, -680px, 0) scale(1.2); opacity: 0; }
    }

    /* Actual Streamlit login card container */
    .st-key-login_card {
        position: relative;
        z-index: 2;
        width: min(440px, 100%);
        max-width: 440px;
        margin: 0 auto;
        padding: 27px 30px 24px;
        box-sizing: border-box;
        border: 1px solid rgba(255, 190, 150, .30);
        border-radius: 27px;
        background: linear-gradient(145deg, rgba(28, 29, 43, .88), rgba(17, 21, 34, .86));
        box-shadow: 0 25px 80px rgba(0,0,0,.48), inset 0 1px 0 rgba(255,255,255,.10);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
    }

    .login-mark {
        width: 54px;
        height: 54px;
        margin: 0 auto 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 18px;
        color: #ffe1c0;
        font-size: 28px;
        background: linear-gradient(145deg, rgba(255,117,57,.35), rgba(255,54,92,.17));
        border: 1px solid rgba(255,174,124,.48);
        box-shadow: 0 0 30px rgba(255,95,50,.22);
    }

    .login-brand {
        font-family: 'Kaushan Script', cursive;
        font-size: clamp(35px, 7vw, 49px);
        line-height: 1.22;
        font-weight: 400;
        letter-spacing: 1px;
        text-align: center;
        background: linear-gradient(100deg, #ffe0a8 5%, #ff9a70 42%, #ff6b9b 72%, #b8a4ff 100%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        filter: drop-shadow(0 0 17px rgba(255,116,112,.24));
    }

    .login-tagline {
        margin-top: 8px;
        margin-bottom: 17px;
        color: #d2cddd;
        font-size: 10px;
        letter-spacing: 2.5px;
        text-align: center;
    }

    .login-note {
        color: #d4d1df;
        font-size: 13px;
        text-align: center;
        margin-bottom: 14px;
    }

    .st-key-login_card label {
        color: #f0eaf0 !important;
    }

    /* Login inputs: light field + dark typed text */
    .st-key-login_card [data-testid="stTextInput"] input {
        background: #ffffff !important;
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
        caret-color: #8b3d70 !important;
        border: 1px solid rgba(255, 174, 145, .55) !important;
        border-radius: 12px !important;
    }

    .st-key-login_card [data-testid="stTextInput"] input::placeholder {
        color: #667085 !important;
        -webkit-text-fill-color: #667085 !important;
        opacity: 1 !important;
    }

    .st-key-login_card [data-testid="stTextInput"] input:focus {
        border-color: #ff9b83 !important;
        box-shadow: 0 0 0 1px #ff9b83 !important;
    }

    .st-key-login_card [data-testid="stFormSubmitButton"] button {
        width: 100%;
        min-height: 47px;
        border: 1px solid rgba(255,190,160,.48);
        border-radius: 13px;
        color: #211522 !important;
        font-weight: 800;
        background: linear-gradient(100deg, #ffd49a, #ff9679, #ff7e9e);
        transition: transform .2s ease, filter .2s ease;
    }

    .st-key-login_card [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px);
        filter: brightness(1.08);
    }

    .login-small {
        color: #bdb8cc;
        font-size: 11px;
        text-align: center;
        margin-top: 13px;
    }

    .login-footer {
        position: relative;
        z-index: 2;
        color: rgba(238,220,224,.76);
        font-size: 11px;
        letter-spacing: .5px;
        text-align: center;
        margin-top: 13px;
    }

    /* ============================================================
       HOME SCREEN - AURORA / COSMIC MOVEMENT (NO FIRE)
       ============================================================ */

    .st-key-home_stage {
        position: relative;
        isolation: isolate;
        overflow: hidden;
        width: 100%;
        min-height: calc(100vh - 2.5rem);
        box-sizing: border-box;
        border-radius: 28px;
        padding: 28px;
        background:
            radial-gradient(ellipse at 12% 18%, rgba(242, 229, 203, .72), transparent 34%),
            radial-gradient(ellipse at 82% 74%, rgba(75, 190, 183, .38), transparent 40%),
            linear-gradient(132deg, #d8d5cd 0%, #9ca7a8 25%, #596c78 54%, #263746 78%, #202b38 100%);
        background-size: 220% 220%;
        animation: homeSurfaceFlow 12s ease-in-out infinite alternate;
    }

    @keyframes homeSurfaceFlow {
        0% { background-position: 0% 15%; }
        50% { background-position: 70% 55%; }
        100% { background-position: 100% 85%; }
    }

    .st-key-home_stage::before,
    .st-key-home_stage::after {
        content: "";
        position: absolute;
        z-index: -1;
        width: 88%;
        height: 78%;
        border-radius: 48%;
        filter: blur(34px);
        opacity: .72;
        pointer-events: none;
    }

    .st-key-home_stage::before {
        left: -20%;
        top: -20%;
        background: linear-gradient(112deg, rgba(247,226,187,.92), rgba(69,208,190,.78), rgba(91,139,224,.76), rgba(174,132,220,.72));
        animation: auroraDrift 10s ease-in-out infinite alternate;
    }

    .st-key-home_stage::after {
        right: -20%;
        bottom: -25%;
        background: linear-gradient(118deg, rgba(63,184,178,.72), rgba(119,151,213,.78), rgba(201,151,190,.72), rgba(234,197,143,.82));
        animation: auroraDrift 12s ease-in-out infinite alternate-reverse;
    }

    @keyframes auroraDrift {
        0% { transform: translate3d(-5%, 4%, 0) rotate(-8deg) scale(.92); }
        50% { transform: translate3d(9%, -6%, 0) rotate(8deg) scale(1.12); }
        100% { transform: translate3d(-2%, 9%, 0) rotate(-3deg) scale(1.04); }
    }

    .home-stars {
        position: absolute;
        inset: 0;
        z-index: -1;
        pointer-events: none;
        overflow: hidden;
    }

    .home-aurora {
        position: absolute;
        display: block;
        width: 125%;
        height: 24%;
        left: -12%;
        border-radius: 50%;
        pointer-events: none;
        mix-blend-mode: screen;
        filter: blur(13px);
        opacity: .58;
        transform-origin: center;
    }
    .home-aurora-one {
        top: 18%;
        background: linear-gradient(90deg, transparent 0%, rgba(75,230,210,.06) 12%, rgba(72,220,205,.72) 38%, rgba(111,158,255,.62) 62%, rgba(205,158,239,.40) 78%, transparent 100%);
        animation: auroraRibbonOne 9s ease-in-out infinite alternate;
    }
    .home-aurora-two {
        top: 47%;
        height: 18%;
        opacity: .46;
        background: linear-gradient(90deg, transparent, rgba(243,204,143,.12) 16%, rgba(245,205,151,.70) 42%, rgba(110,202,194,.66) 68%, transparent);
        animation: auroraRibbonTwo 12s ease-in-out infinite alternate;
    }
    .home-aurora-three {
        top: 70%;
        height: 22%;
        opacity: .38;
        background: linear-gradient(90deg, transparent, rgba(121,163,244,.62) 30%, rgba(183,143,224,.62) 58%, rgba(76,208,190,.30) 82%, transparent);
        animation: auroraRibbonThree 11s ease-in-out infinite alternate;
    }
    @keyframes auroraRibbonOne {
        0% { transform: translate3d(-8%, 12px, 0) rotate(-9deg) scaleY(.72); }
        100% { transform: translate3d(9%, -24px, 0) rotate(7deg) scaleY(1.18); }
    }
    @keyframes auroraRibbonTwo {
        0% { transform: translate3d(8%, -18px, 0) rotate(8deg) scaleY(1.05); }
        100% { transform: translate3d(-7%, 20px, 0) rotate(-8deg) scaleY(.72); }
    }
    @keyframes auroraRibbonThree {
        0% { transform: translate3d(-5%, 14px, 0) rotate(6deg) scaleY(.8); }
        100% { transform: translate3d(7%, -15px, 0) rotate(-6deg) scaleY(1.12); }
    }
    @media (prefers-reduced-motion: reduce) {
        .st-key-home_stage, .st-key-home_stage::before, .st-key-home_stage::after,
        .home-aurora, .home-star, .st-key-maths_tutor_shell { animation: none !important; }
    }

    .home-star {
        position: absolute;
        display: block;
        width: 4px;
        height: 4px;
        border-radius: 50%;
        background: #e3ffff;
        box-shadow: 0 0 12px 3px rgba(157, 241, 255, .45);
        animation: starFloat 9s ease-in-out infinite;
    }

    .home-star:nth-child(1) { left: 8%; top: 18%; animation-delay: -2s; }
    .home-star:nth-child(2) { left: 19%; top: 72%; width: 3px; height: 3px; animation-delay: -5s; }
    .home-star:nth-child(3) { left: 34%; top: 28%; animation-delay: -1s; }
    .home-star:nth-child(4) { left: 48%; top: 82%; width: 5px; height: 5px; animation-delay: -7s; }
    .home-star:nth-child(5) { left: 63%; top: 16%; width: 3px; height: 3px; animation-delay: -3s; }
    .home-star:nth-child(6) { left: 78%; top: 61%; animation-delay: -6s; }
    .home-star:nth-child(7) { left: 91%; top: 31%; width: 3px; height: 3px; animation-delay: -4s; }
    .home-star:nth-child(8) { left: 55%; top: 45%; width: 3px; height: 3px; animation-delay: -8s; }
    .home-star:nth-child(9) { left: 27%; top: 48%; width: 5px; height: 5px; animation-delay: -3s; }
    .home-star:nth-child(10) { left: 86%; top: 84%; width: 3px; height: 3px; animation-delay: -1s; }

    @keyframes starFloat {
        0%, 100% { transform: translate3d(0, 0, 0); opacity: .25; }
        50% { transform: translate3d(13px, -22px, 0); opacity: 1; }
    }

    .home-heading {
        font-family: 'Kaushan Script', cursive;
        font-size: clamp(38px, 6vw, 58px);
        font-weight: 400;
        letter-spacing: .02em;
        text-align: center;
        margin-top: clamp(18px, 3vh, 34px);
        background: linear-gradient(100deg, #fff1c8 5%, #a8f5ee 48%, #d6c4ff 95%);
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-shadow: 0 5px 25px rgba(0,0,0,.18);
        filter: drop-shadow(0 3px 16px rgba(0,0,0,.16));
    }

    .home-subheading {
        color: #e7edf0;
        text-align: center;
        font-size: 13px;
        letter-spacing: 1.2px;
        margin-top: 9px;
        margin-bottom: 28px;
    }

    .home-welcome {
        color: #f0f3f4;
        text-align: center;
        font-size: 14px;
        margin-bottom: 24px;
    }

    .st-key-open_ai_button button,
    .st-key-home_logout button,
    .st-key-chat_home_button button {
        border-radius: 12px !important;
        min-height: 45px !important;
        font-weight: 700 !important;
    }

    .st-key-open_ai_button button {
        min-width: 250px !important;
        min-height: 58px !important;
        padding: 0 26px !important;
        border-radius: 15px !important;
        color: #14263d !important;
        border: 1px solid rgba(205,255,255,.75) !important;
        background: linear-gradient(105deg, #a9f4ed, #b7d9ff, #d4c4ff) !important;
        box-shadow: 0 9px 28px rgba(93, 208, 219, .20);
    }

    .st-key-open_ai_button button:hover {
        filter: brightness(1.08);
        transform: translateY(-1px);
    }

    .st-key-home_logout button {
        color: #ffffff !important;
        background: linear-gradient(135deg, #d9233d, #a80f2b) !important;
        border: 1px solid rgba(255, 190, 200, .65) !important;
        border-radius: 13px !important;
        min-height: 48px !important;
        font-weight: 800 !important;
        box-shadow: 0 8px 24px rgba(190, 20, 55, .28);
    }
    .st-key-home_logout { margin-top: clamp(24px, 5vh, 56px); }
    .st-key-open_ai_button button,
    .st-key-maths_tutor_button button {
        width: 100% !important;
        min-width: 0 !important;
        min-height: clamp(128px, 18vw, 190px) !important;
        aspect-ratio: 1 / 1 !important;
        white-space: pre-line !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        line-height: 1.5 !important;
        font-size: clamp(15px, 2vw, 21px) !important;
        border-radius: 22px !important;
        padding: 12px !important;
    }
    .st-key-open_ai_button button {
        max-width: 230px !important;
        margin-inline: auto !important;
        color: #14263d !important;
        border: 1px solid rgba(205,255,255,.82) !important;
        background: linear-gradient(145deg, #b9fff0, #a9d8ff 52%, #d8c5ff) !important;
        box-shadow: 0 12px 30px rgba(73, 170, 205, .24), inset 0 1px 0 rgba(255,255,255,.8) !important;
    }
    .st-key-maths_tutor_button button {
        color: #fff8ff !important;
        border: 1px solid rgba(232,205,255,.82) !important;
        background: linear-gradient(145deg, #563b91, #7651b8 52%, #3f679e) !important;
        box-shadow: 0 12px 30px rgba(77,56,145,.32), inset 0 1px 0 rgba(255,255,255,.2) !important;
        font-family: 'Kaushan Script', cursive !important;
    }
    .st-key-ai_feature_studio_button button {
        width: 100% !important;
        min-height: 62px !important;
        border-radius: 16px !important;
        color: #fff !important;
        font-weight: 800 !important;
        letter-spacing: .04em !important;
        background: linear-gradient(100deg, #263f71, #6b4b9f 52%, #257b83) !important;
        border: 1px solid rgba(224,236,255,.7) !important;
        box-shadow: 0 10px 28px rgba(24,36,80,.28) !important;
    }
    .st-key-chat_home_button button {
        color: #eefaff !important;
        background: rgba(20, 48, 72, .78) !important;
        border: 1px solid rgba(204, 232, 255, .48) !important;
        border-radius: 13px !important;
        min-height: 46px !important;
        padding: 0 18px !important;
    }

    /* ============================================================
       AI CHAT SCREEN - CLEAN WHITE SNOWFALL CANVAS
       ============================================================ */
    [data-testid="stMain"]:has(.chat-snow-layer) {
        background:
            radial-gradient(ellipse at 12% 8%, rgba(135, 190, 231, .22), transparent 36%),
            radial-gradient(ellipse at 88% 28%, rgba(180, 211, 237, .28), transparent 42%),
            radial-gradient(ellipse at 48% 100%, rgba(204, 222, 239, .32), transparent 48%),
            linear-gradient(145deg, #edf5fc 0%, #f8fbff 42%, #eaf2fa 100%) !important;
        background-attachment: fixed !important;
        animation: none !important;
    }

    .hero {
        text-align: center;
        padding: 12px 0 24px;
    }

    .logo {
        width: 58px;
        height: 58px;
        border-radius: 19px;
        margin: auto auto 12px;
        display: flex;
        justify-content: center;
        align-items: center;
        background: linear-gradient(145deg,#31576C,#1A2C40);
        border: 1px solid #6D9DA9;
        color: #B8F3E8;
        font-size: 29px;
        box-shadow: 0 0 30px #77D9CD20;
    }

    .brand {
        color: #20354b;
        font-size: 32px;
        font-weight: 800;
        letter-spacing: 4px;
    }

    .subtitle {
        color: #61778d;
        font-size: 10px;
        letter-spacing: 3px;
        margin-top: 6px;
    }

    /* Chat message cards */
    [data-testid="stChatMessage"] {
        border-radius: 19px;
        padding: 15px;
        margin-bottom: 15px;
        border: 1px solid rgba(177, 211, 239, .34);
        box-shadow: 0 8px 25px rgba(4, 15, 31, .12);
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: rgba(34, 54, 79, .91);
        border-color: rgba(151, 190, 220, .38);
    }

    [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: rgba(47, 76, 105, .94);
        border-color: rgba(164, 204, 231, .42);
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] span {
        color: #F5F8FF !important;
    }

    /* Chat input: pale field with dark text to avoid white-on-white */
    [data-testid="stChatInput"] {
        background: #ffffff !important;
        border: 1px solid #a9c3e0 !important;
        border-radius: 28px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 30px rgba(7, 19, 37, .24), inset 0 1px 0 rgba(255,255,255,.8);
    }
    [data-testid="stChatInput"] > div,
    [data-testid="stChatInput"] textarea {
        border-radius: 26px !important;
    }

    [data-testid="stChatInput"] textarea {
        color: var(--chat-ink) !important;
        -webkit-text-fill-color: var(--chat-ink) !important;
        caret-color: #315e94 !important;
        background: transparent !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #596b82 !important;
        -webkit-text-fill-color: #596b82 !important;
        opacity: 1 !important;
    }

    [data-testid="stChatInput"] button {
        color: #263e5b !important;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #172b43;
        border-right: 1px solid #405a76;
    }

    [data-testid="stSidebar"] * {
        color: #f1f6ff;
    }

    .stButton > button {
        background: #2b4562;
        color: white;
        border: 1px solid #66839f;
        border-radius: 12px;
        min-height: 40px;
    }

    .stButton > button:hover {
        background: #3a5c7c;
        border-color: #8bdedb;
        color: white;
    }

    .footer {
        text-align: center;
        color: #d0dfef;
        font-size: 11px;
        padding: 22px 0;
    }


    /* Snowflake-only overlay: no winter scenery, watermark, or background tint */
    .chat-snow-layer {
        position: fixed;
        inset: 0;
        z-index: 0;
        overflow: hidden;
        pointer-events: none;
        background: transparent;
    }
    .chat-snowflake {
        position: absolute;
        top: -30px;
        display: block;
        width: var(--flake-size, 8px);
        height: var(--flake-size, 8px);
        color: rgba(75, 139, 190, .92);
        opacity: var(--flake-opacity, .82);
        text-shadow: 0 1px 0 rgba(255,255,255,.95), 0 2px 7px rgba(66,126,174,.32);
        filter: drop-shadow(0 2px 4px rgba(75, 125, 165, .25));
        animation: snowFall var(--fall-duration, 12s) linear infinite;
        animation-delay: var(--fall-delay, 0s);
    }
    .chat-snowflake::before {
        content: "❄";
        position: absolute;
        left: 50%;
        top: 50%;
        transform: translate(-50%, -50%);
        font-size: calc(var(--flake-size, 8px) * 2.2);
        line-height: 1;
    }
    @keyframes snowFall {
        0% { transform: translate3d(0, -5vh, 0) rotate(0deg); }
        25% { transform: translate3d(24px, 25vh, 0) rotate(90deg); }
        50% { transform: translate3d(-18px, 52vh, 0) rotate(180deg); }
        75% { transform: translate3d(22px, 78vh, 0) rotate(270deg); }
        100% { transform: translate3d(-10px, 112vh, 0) rotate(360deg); }
    }
    [data-testid="stMain"]:has(.chat-snow-layer) .stMainBlockContainer {
        position: relative;
        z-index: 1;
    }
    @media (max-width: 600px) {
        .st-key-open_ai_button button {
            min-width: 0 !important;
            width: 100% !important;
            padding: 0 12px !important;
        }
    }


    /* ============================================================
       CHAT: CLEAN WHITE CANVAS WITH ONLY FALLING SNOWFLAKES
       ============================================================ */
    [data-testid="stMain"]:has(.chat-snow-layer),
    [data-testid="stAppViewContainer"]:has(.chat-snow-layer),
    [data-testid="stMain"]:has(.chat-snow-layer) > div {
        background-color: #f3f8fd !important;
        background-image:
            radial-gradient(ellipse at 10% 12%, rgba(135,190,231,.16), transparent 35%),
            radial-gradient(ellipse at 90% 70%, rgba(183,211,235,.20), transparent 40%),
            linear-gradient(145deg, rgba(236,245,253,.96), rgba(249,252,255,.97) 48%, rgba(232,241,250,.96)) !important;
        animation: none !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) {
        color: #20354b !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) .stMarkdown,
    [data-testid="stMain"]:has(.chat-snow-layer) .stMarkdown p,
    [data-testid="stMain"]:has(.chat-snow-layer) .stMarkdown li,
    [data-testid="stMain"]:has(.chat-snow-layer) label,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stCaptionContainer"] {
        color: #263e55 !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) .hero .brand,
    [data-testid="stMain"]:has(.chat-snow-layer) .hero .subtitle {
        color: #20354b !important;
        text-shadow: none !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) .logo {
        background: #e5f2fc !important;
        border-color: #b7d2e8 !important;
        color: #345b7d !important;
        box-shadow: none !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] {
        background: linear-gradient(145deg, rgba(255,255,255,.98), rgba(242,248,253,.96)) !important;
        border: 1px solid #cbdceb !important;
        box-shadow: 0 7px 22px rgba(40,75,105,.10), inset 0 1px 0 rgba(255,255,255,.95) !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"],
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] *,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] p,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] li,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] strong,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] span,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] code,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] a {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) .footer {
        color: #61778d !important;
    }
    .chat-snowflake { color: rgba(66,132,184,.92) !important; opacity: .86 !important; text-shadow: 0 1px 0 #fff, 0 2px 8px rgba(65,125,175,.35) !important; filter: drop-shadow(0 2px 4px rgba(70,120,165,.24)) !important; }
    .chat-snowflake::before { content: "❄"; }

    /* Loading spinner appearance */
    .stSpinner > div {
        border-top-color: #4f91c4 !important;
    }

    /* Mobile layout */
    @media (max-width: 600px) {
        .block-container {
            padding: .55rem .55rem 2rem;
        }

        .st-key-login_stage {
            min-height: calc(100svh - 1.5rem);
            border-radius: 20px;
            padding: 15px 10px;
        }

        .st-key-login_card {
            padding: 23px 18px 20px;
            border-radius: 22px;
        }

        .login-brand {
            font-size: 37px;
        }

        .st-key-home_stage {
            min-height: calc(100svh - 1.5rem);
            border-radius: 20px;
            padding: 15px;
        }

        .home-heading {
            margin-top: 2vh;
            font-size: clamp(35px, 10vw, 46px);
        }
        .st-key-open_ai_button button,
        .st-key-maths_tutor_button button {
            min-height: 126px !important;
            font-size: 15px !important;
            border-radius: 17px !important;
        }

        .brand {
            font-size: 27px;
        }

        [data-testid="stChatMessage"] {
            padding: 12px;
        }
    }

    @media (max-height: 700px) and (min-width: 601px) {
        .st-key-login_stage {
            min-height: calc(100vh - 2rem);
            padding-top: 12px;
            padding-bottom: 12px;
        }

        .st-key-login_card {
            padding-top: 19px;
            padding-bottom: 17px;
        }

        .login-mark {
            width: 46px;
            height: 46px;
            margin-bottom: 8px;
        }

        .login-tagline {
            margin-bottom: 10px;
        }
    }

    /* ============================================================
       FINAL CHAT TEXT OVERRIDE - BLACK TEXT IN BOTH MESSAGE TYPES
       ============================================================ */
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] *,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] p,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] li,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] strong,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] em,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] span,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] code,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] pre,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] a,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] h1,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] h2,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] h3 {
        color: #111827 !important;
        -webkit-text-fill-color: #111827 !important;
    }

    /* Maths Tutor launcher: elegant cursive lettering and a distinct violet-blue theme */
    .st-key-maths_tutor_button button {
        width: 100% !important;
        max-width: 230px !important;
        min-width: 0 !important;
        min-height: clamp(128px, 18vw, 190px) !important;
        aspect-ratio: 1 / 1 !important;
        white-space: pre-line !important;
        padding: 12px !important;
        margin-inline: auto !important;
        border-radius: 22px !important;
        color: #fff8ff !important;
        -webkit-text-fill-color: #fff8ff !important;
        font-family: 'Kaushan Script', cursive !important;
        font-size: clamp(15px, 2vw, 21px) !important;
        line-height: 1.5 !important;
        letter-spacing: .4px !important;
        border: 1px solid rgba(232, 205, 255, .85) !important;
        background: linear-gradient(115deg, #563b91 0%, #7651b8 48%, #3f679e 100%) !important;
        box-shadow: 0 10px 28px rgba(77, 56, 145, .34), inset 0 1px 0 rgba(255,255,255,.22) !important;
        transition: transform .2s ease, filter .2s ease, box-shadow .2s ease !important;
    }
    .st-key-maths_tutor_button button:hover {
        filter: brightness(1.12) !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 14px 32px rgba(77, 56, 145, .42) !important;
    }

    /* Dedicated Maths Tutor page */
    .st-key-maths_tutor_shell {
        position: relative;
        isolation: isolate;
        overflow: hidden;
        border-radius: 25px;
        padding: 20px 18px 24px;
        background:
            radial-gradient(ellipse at 8% 8%, rgba(126, 174, 177, .25), transparent 36%),
            radial-gradient(ellipse at 92% 88%, rgba(164, 139, 190, .23), transparent 40%),
            radial-gradient(ellipse at 48% 52%, rgba(91, 112, 128, .20), transparent 54%),
            linear-gradient(145deg, #182a37 0%, #263746 48%, #302c3d 100%);
        border: 1px solid rgba(174, 197, 203, .42);
        box-shadow: 0 18px 44px rgba(5, 12, 22, .32), inset 0 1px 0 rgba(255,255,255,.07);
        background-size: 180% 180%;
        animation: tutorAtmosphere 16s ease-in-out infinite alternate;
    }
    @keyframes tutorAtmosphere {
        0% { background-position: 0% 10%; }
        100% { background-position: 100% 90%; }
    }
    .maths-tutor-title {
        color: #e8e5f1;
        font-family: 'Kaushan Script', cursive;
        font-size: clamp(34px, 6vw, 48px);
        text-align: center;
        line-height: 1.25;
        margin: 10px 0 5px;
        text-shadow: 0 4px 18px rgba(0, 0, 0, .30);
    }
    .maths-tutor-subtitle {
        color: #bdcbd3;
        font-size: 12px;
        letter-spacing: 1.7px;
        text-align: center;
        margin-bottom: 22px;
    }
    .st-key-maths_tutor_shell .stMarkdown,
    .st-key-maths_tutor_shell .stMarkdown p,
    .st-key-maths_tutor_shell label,
    .st-key-maths_tutor_shell [data-testid="stCaptionContainer"] {
        color: #e4ebef !important;
    }
    .st-key-maths_tutor_shell [data-testid="stChatMessage"] {
        background: linear-gradient(145deg, rgba(224, 229, 227, .97), rgba(205, 214, 214, .96)) !important;
        border: 1px solid rgba(238, 244, 241, .72) !important;
        border-radius: 20px !important;
        box-shadow: 0 9px 24px rgba(4, 12, 22, .20), inset 0 1px 0 rgba(255,255,255,.72) !important;
    }
    .st-key-maths_tutor_shell [data-testid="stChatMessage"],
    .st-key-maths_tutor_shell [data-testid="stChatMessage"] *,
    .st-key-maths_tutor_shell [data-testid="stChatMessage"] p,
    .st-key-maths_tutor_shell [data-testid="stChatMessage"] li,
    .st-key-maths_tutor_shell [data-testid="stChatMessage"] strong,
    .st-key-maths_tutor_shell [data-testid="stChatMessage"] span,
    .st-key-maths_tutor_shell [data-testid="stChatMessage"] code {
        color: #172033 !important;
        -webkit-text-fill-color: #172033 !important;
    }
    .st-key-maths_tutor_shell [data-testid="stChatInput"] {
        background: #ffffff !important;
        border: 1px solid rgba(174, 205, 205, .92) !important;
        border-radius: 30px !important;
        overflow: hidden !important;
        box-shadow: 0 10px 26px rgba(4, 12, 22, .24), inset 0 1px 0 rgba(255,255,255,.9) !important;
    }
    .st-key-maths_tutor_shell [data-testid="stChatInput"] > div,
    .st-key-maths_tutor_shell [data-testid="stChatInput"] textarea {
        border-radius: 28px !important;
    }
    .st-key-maths_tutor_shell [data-testid="stChatInput"] textarea {
        color: #17252d !important;
        -webkit-text-fill-color: #17252d !important;
        caret-color: #477e83 !important;
        background: transparent !important;
    }
    .st-key-maths_tutor_shell [data-testid="stChatInput"] textarea::placeholder {
        color: #596a70 !important;
        -webkit-text-fill-color: #596a70 !important;
    }
    .st-key-maths_tutor_back button {
        color: #fff !important;
        background: linear-gradient(110deg, #554080, #426d9b) !important;
        border: 1px solid #b7a6dc !important;
    }
    @media (max-width: 600px) {
        .st-key-maths_tutor_button button {
            min-width: 0 !important;
            max-width: 100% !important;
            width: 100% !important;
            min-height: 126px !important;
            font-size: 15px !important;
        }
        .st-key-maths_tutor_shell {
            padding: 14px 10px 18px;
            border-radius: 19px;
        }
    }


    /* Universal tactile 3D button finish */
    .stButton > button,
    [data-testid="stFormSubmitButton"] button {
        position: relative !important;
        border-width: 1px !important;
        border-style: solid !important;
        transform: translateY(0) !important;
        box-shadow: 0 5px 0 rgba(8, 18, 35, .34), 0 9px 18px rgba(8, 18, 35, .22), inset 0 1px 0 rgba(255,255,255,.30) !important;
        transition: transform .14s ease, box-shadow .14s ease, filter .14s ease !important;
    }
    .stButton > button:hover,
    [data-testid="stFormSubmitButton"] button:hover {
        transform: translateY(-2px) !important;
        filter: brightness(1.06) !important;
        box-shadow: 0 7px 0 rgba(8, 18, 35, .30), 0 13px 22px rgba(8, 18, 35, .24), inset 0 1px 0 rgba(255,255,255,.34) !important;
    }
    .stButton > button:active,
    [data-testid="stFormSubmitButton"] button:active {
        transform: translateY(3px) !important;
        box-shadow: 0 2px 0 rgba(8, 18, 35, .34), 0 4px 9px rgba(8, 18, 35, .18), inset 0 1px 2px rgba(0,0,0,.12) !important;
    }

    /* Highest-priority chat message text color: both user and assistant messages */
    [data-testid="stChatMessage"],
    [data-testid="stChatMessage"] *,
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"],
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] *,
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] em,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] code,
    [data-testid="stChatMessage"] pre,
    [data-testid="stChatMessage"] a,
    [data-testid="stChatMessage"] h1,
    [data-testid="stChatMessage"] h2,
    [data-testid="stChatMessage"] h3 {
        color: #111111 !important;
        -webkit-text-fill-color: #111111 !important;
        opacity: 1 !important;
    }
    [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] * {
        text-shadow: none !important;
    }

    /* Auth mode switch button */
    .st-key-auth_mode_switch button {
        color: #ffe5d3 !important;
        background: linear-gradient(145deg, #45304b, #28283f) !important;
        border: 1px solid rgba(255,190,160,.48) !important;
    }



    /* ============================================================
       MY AI FEATURE STUDIO — DISTINCT ANIMATED ENVIRONMENTS
       Existing mobile.app styles and component are left untouched.
       ============================================================ */
    .feature-title {
        font-family: 'Kaushan Script', cursive !important;
        font-size: clamp(2rem, 5vw, 3.15rem) !important;
        line-height: 1.2;
        letter-spacing: .01em;
        color: #fff7d6 !important;
        text-shadow: 0 3px 22px rgba(0,0,0,.48), 0 0 26px rgba(255,255,255,.16);
        margin: 12px 0 5px;
    }
    .feature-subtitle {
        color: #e4efff !important;
        font-size: .78rem;
        font-weight: 800;
        letter-spacing: .18em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }
    .feature-copy, .feature-copy p, .feature-copy li {
        color: #f2f6ff !important;
        line-height: 1.65;
    }
    [class*="st-key-feature_"] {
        position: relative;
        isolation: isolate;
        overflow: hidden;
        border: 1px solid rgba(255,255,255,.2);
        border-radius: 26px;
        padding: clamp(16px, 3vw, 28px);
        min-height: 0;
        box-shadow: 0 22px 70px rgba(0,0,0,.25);
    }
    [class*="st-key-feature_"] > div { position: relative; z-index: 1; }
    [class*="st-key-feature_"]::before,
    [class*="st-key-feature_"]::after {
        content: ""; position: absolute; z-index: 0; pointer-events: none;
        inset: -25%; opacity: .72; filter: blur(35px);
    }
    .st-key-feature_hub {
        background: radial-gradient(circle at 15% 15%,#4564a8 0,transparent 36%),
                    radial-gradient(circle at 85% 80%,#6d3d91 0,transparent 34%),
                    linear-gradient(135deg,#101a35,#172d4d 55%,#271c48);
    }
    .st-key-feature_hub::before { background: conic-gradient(from 0deg,transparent,#52d6d0aa,transparent,#ad7bffaa,transparent); animation: hubOrbit 18s linear infinite; }
    .st-key-feature_voice { background: radial-gradient(ellipse at 50% 110%,#ff9b55 0,transparent 45%),linear-gradient(145deg,#26132e,#542044 48%,#182c52); }
    .st-key-feature_voice::before { background: repeating-radial-gradient(ellipse at 50% 50%,#ffbd7955 0 2px,transparent 3px 24px); animation: voicePulse 8s ease-in-out infinite; }
    .st-key-feature_voice::after { background: linear-gradient(110deg,transparent,#ff8f6b55,transparent); animation: voiceSweep 7s ease-in-out infinite; }
    .st-key-feature_search { background: radial-gradient(circle at 75% 20%,#247e9d 0,transparent 38%),linear-gradient(135deg,#071e32,#103f5c 55%,#102b4b); }
    .st-key-feature_search::before { background: repeating-linear-gradient(0deg,transparent 0 42px,#61e5ef22 43px 44px),repeating-linear-gradient(90deg,transparent 0 42px,#61e5ef22 43px 44px); transform: perspective(500px) rotateX(58deg) scale(1.8); animation: searchGrid 12s linear infinite; }
    .st-key-feature_image { background: radial-gradient(ellipse at 15% 20%,#ff6cba 0,transparent 35%),radial-gradient(ellipse at 90% 85%,#7669ff 0,transparent 42%),linear-gradient(135deg,#24153e,#43265c 55%,#192a52); }
    .st-key-feature_image::before { background: conic-gradient(from 30deg,transparent,#ff9bd088,#9e8aff88,transparent); animation: imagePrism 14s ease-in-out infinite alternate; }
    .st-key-feature_presentation { background: radial-gradient(ellipse at 20% 90%,#d29b47 0,transparent 38%),linear-gradient(140deg,#171b36,#34406b 50%,#543a62); }
    .st-key-feature_presentation::before { background: linear-gradient(115deg,transparent 20%,#ffe0a044 45%,transparent 65%); animation: slideLight 9s ease-in-out infinite; }
    .st-key-feature_data { background: radial-gradient(circle at 80% 20%,#25b6a5 0,transparent 35%),linear-gradient(145deg,#071f2b,#104d56 55%,#163a50); }
    .st-key-feature_data::before { background: repeating-linear-gradient(90deg,transparent 0 7%,#6af3ce18 7.2% 7.5%),linear-gradient(0deg,transparent 48%,#66eac044 49%,transparent 50%); animation: dataFlow 10s linear infinite; }
    .st-key-feature_pdf { background: radial-gradient(ellipse at 80% 15%,#bd704f 0,transparent 35%),linear-gradient(145deg,#291a1c,#57302e 50%,#252b45); }
    .st-key-feature_pdf::before { background: repeating-linear-gradient(135deg,transparent 0 34px,#ffd2a51c 35px 37px); animation: paperDrift 16s linear infinite; }
    @keyframes hubOrbit { to { transform: rotate(360deg) scale(1.1); } }
    @keyframes voicePulse { 0%,100% { transform:scale(.78); opacity:.35; } 50% { transform:scale(1.2); opacity:.85; } }
    @keyframes voiceSweep { 0% { transform:translateX(-35%) rotate(-12deg); } 100% { transform:translateX(35%) rotate(-12deg); } }
    @keyframes searchGrid { from { background-position:0 0; } to { background-position:0 84px; } }
    @keyframes imagePrism { from { transform:translate(-8%,5%) rotate(-10deg) scale(.9); } to { transform:translate(9%,-6%) rotate(18deg) scale(1.15); } }
    @keyframes slideLight { 0% { transform:translateX(-45%) rotate(8deg); } 100% { transform:translateX(45%) rotate(8deg); } }
    @keyframes dataFlow { from { transform:translateY(-5%) translateX(-2%); } to { transform:translateY(5%) translateX(2%); } }
    @keyframes paperDrift { from { transform:translate(-2%,-2%); } to { transform:translate(2%,2%); } }
    [class*="st-key-feature_"] [data-testid="stMarkdownContainer"],
    [class*="st-key-feature_"] label,
    [class*="st-key-feature_"] p,
    [class*="st-key-feature_"] li,
    [class*="st-key-feature_"] small { color: #f5f7ff !important; }
    [class*="st-key-feature_"] [data-testid="stWidgetLabel"] p { color:#fff7dc !important; font-weight:700; }
    [class*="st-key-feature_"] input,
    [class*="st-key-feature_"] textarea,
    [class*="st-key-feature_"] [data-baseweb="input"] > div,
    [class*="st-key-feature_"] [data-baseweb="textarea"] > div,
    [class*="st-key-feature_"] [data-baseweb="select"] > div {
        background:#ffffff !important;
        color:#17243a !important;
        -webkit-text-fill-color:#17243a !important;
        caret-color:#17243a !important;
        border:1px solid rgba(255,255,255,.82) !important;
        border-radius:12px !important;
    }
    [class*="st-key-feature_"] input::placeholder,
    [class*="st-key-feature_"] textarea::placeholder {
        color:#66758a !important;
        -webkit-text-fill-color:#66758a !important;
        opacity:1 !important;
    }
    [class*="st-key-feature_"] [data-baseweb="select"] *,
    [class*="st-key-feature_"] [role="option"] {
        color:#17243a !important;
        -webkit-text-fill-color:#17243a !important;
    }
    [class*="st-key-feature_"] [role="option"] { background:#ffffff !important; }
    [class*="st-key-feature_"] button {
        border:1px solid rgba(255,255,255,.35) !important;
        background:linear-gradient(135deg,rgba(255,255,255,.19),rgba(255,255,255,.08)) !important;
        color:#fff !important; font-weight:700 !important; border-radius:13px !important;
    }
    [class*="st-key-feature_"] [data-testid="stFileUploader"] section {
        background:rgba(255,255,255,.1); border:1px dashed rgba(255,255,255,.55); border-radius:14px;
    }
    @media (max-width: 720px) {
        [class*="st-key-feature_"] {
            min-height: auto;
            padding: 15px 12px 20px;
            border-radius: 19px;
        }
        .feature-title { font-size: clamp(1.8rem, 8vw, 2.5rem) !important; }
        .feature-subtitle { letter-spacing: .11em; font-size: .68rem; }
        [class*="st-key-feature_"] [data-testid="stHorizontalBlock"] {
            gap: .55rem;
        }
    }
    @media (prefers-reduced-motion: reduce) {
        [class*="st-key-feature_"]::before, [class*="st-key-feature_"]::after,
        .st-key-home_stage, .st-key-home_stage::before, .st-key-home_stage::after,
        .home-aurora, .home-star { animation:none !important; }
    }

    /* Final polish: legible input text, soft edges, clear chat-card contrast. */
    [data-testid="stMain"] input,
    [data-testid="stMain"] textarea,
    [data-testid="stMain"] [data-baseweb="input"] > div,
    [data-testid="stMain"] [data-baseweb="textarea"] > div,
    [data-testid="stMain"] [data-testid="stChatInput"] {
        border-radius: 15px !important;
    }
    [data-testid="stMain"] input,
    [data-testid="stMain"] textarea,
    [data-testid="stMain"] [data-testid="stChatInput"] textarea {
        color: #17243a !important;
        -webkit-text-fill-color: #17243a !important;
        caret-color: #315b91 !important;
        background-color: #ffffff !important;
    }
    [data-testid="stMain"] input::placeholder,
    [data-testid="stMain"] textarea::placeholder,
    [data-testid="stMain"] [data-testid="stChatInput"] textarea::placeholder {
        color: #65758b !important;
        -webkit-text-fill-color: #65758b !important;
        opacity: 1 !important;
    }
    [data-testid="stMain"] input:focus,
    [data-testid="stMain"] textarea:focus,
    [data-testid="stMain"] [data-testid="stChatInput"]:focus-within {
        outline: none !important;
        border-color: #76a9df !important;
        box-shadow: 0 0 0 3px rgba(118,169,223,.22) !important;
    }
    [data-testid="stMain"] [data-testid="stChatMessage"] {
        border-radius: 19px !important;
        overflow-wrap: anywhere !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) {
        background: linear-gradient(145deg,#edf6ff,#e2eefb) !important;
        border-color: #c5d9ec !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
        background: linear-gradient(145deg,#fff8e9,#f7edd9) !important;
        border-color: #e7d7b9 !important;
    }
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] *,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] p,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] li,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] strong,
    [data-testid="stMain"]:has(.chat-snow-layer) [data-testid="stChatMessage"] code {
        color: #17243a !important;
        -webkit-text-fill-color: #17243a !important;
    }
    [data-testid="stMain"] [data-testid="stFileUploader"] section {
        border-radius: 16px !important;
    }
    [data-testid="stMain"] .stButton > button {
        border-radius: 15px !important;
    }
    @media (max-width: 720px) {
        .block-container { padding-left: .65rem !important; padding-right: .65rem !important; }
        [data-testid="stMain"] [data-testid="stChatMessage"] { padding: 12px !important; }
        .feature-title { overflow-wrap: anywhere; }
    }
    @media (prefers-reduced-motion: reduce) {
        [data-testid="stMain"], [data-testid="stMain"] * {
            scroll-behavior: auto !important;
        }
    }

    </style>
    """, unsafe_allow_html=True)


    # ============================================================
    # HOME / AI LAUNCHER PAGE
    # ============================================================

    if st.session_state.current_page == "home":
        with st.container(key="home_stage"):
            st.markdown("""
            <div class="home-stars">
                <span class="home-aurora home-aurora-one"></span>
                <span class="home-aurora home-aurora-two"></span>
                <span class="home-aurora home-aurora-three"></span>
                <span class="home-star"></span>
                <span class="home-star"></span>
                <span class="home-star"></span>
                <span class="home-star"></span>
                <span class="home-star"></span>
                <span class="home-star"></span>
                <span class="home-star"></span>
                <span class="home-star"></span>
                <span class="home-star"></span>
                <span class="home-star"></span>
            </div>
            """, unsafe_allow_html=True)

            st.markdown("""
            <div class="home-heading">KASHAN'S AI</div>
            <div class="home-subheading">
                YOUR PERSONAL INTELLIGENCE SPACE
            </div>
            """, unsafe_allow_html=True)

            st.markdown(
                "<div class=\"home-welcome\">Welcome to KASHAN'S AI.</div>",
                unsafe_allow_html=True
            )

            # Two equal launch tiles; the studio remains a separate full-width action.
            launcher_left, launcher_right = st.columns(2, gap="medium")
            with launcher_left:
                if st.button(
                    "✦\nOPEN AI CHAT",
                    key="open_ai_button",
                    use_container_width=True
                ):
                    st.session_state.current_page = "chat"
                    st.rerun()
            with launcher_right:
                if st.button(
                    "✧\nMaths Tutor",
                    key="maths_tutor_button",
                    use_container_width=True
                ):
                    st.session_state.current_page = "maths_tutor"
                    st.rerun()

            if st.button(
                "✧  OPEN AI FEATURE STUDIO  →",
                key="ai_feature_studio_button",
                use_container_width=True
            ):
                st.session_state.current_page = "ai_tools"
                st.rerun()



        st.stop()




    # ============================================================
    # AI FEATURE STUDIO — SIX ADD-ON TOOLS
    # All feature logic is isolated from the original mobile app and
    # the existing chat / maths tutor workflows.
    # ============================================================

    def _feature_go_home():
        if st.button("← AI Studio", key="feature_back_to_studio", use_container_width=False):
            st.session_state.current_page = "ai_tools"
            st.rerun()

    def _feature_groq_client():
        try:
            return Groq(api_key=st.secrets["GROQ_API_KEY"])
        except Exception:
            st.error("AI connection failed. Please check GROQ_API_KEY in Streamlit Secrets.")
            return None

    def _feature_ai_text(client, prompt, system_prompt=None, max_tokens=2200):
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        response = client.chat.completions.create(
            model=CHAT_MODEL,
            messages=messages,
            temperature=0.35,
            max_tokens=max_tokens,
        )
        return response.choices[0].message.content or "I could not generate a response."

    if st.session_state.current_page == "ai_tools":
        with st.container(key="feature_hub"):
            st.markdown('<div class="feature-title">AI Feature Studio</div><div class="feature-subtitle">Five tools · one workspace</div>', unsafe_allow_html=True)
            st.markdown('<div class="feature-copy">Choose a tool to open its own workspace. Each tool has a distinct animated environment.</div>', unsafe_allow_html=True)
            st.write("")
            # Image Understanding stays in the code and can be re-enabled later.
            cards = [
                ("🎙️ Voice Conversation", "voice_feature", "feature_voice"),
                ("🌐 Live Web Search", "search_feature", "feature_search"),
                ("📊 Presentation Maker", "presentation_feature", "feature_presentation"),
                ("📈 Data Analyst", "data_feature", "feature_data"),
                ("📚 PDF Expert", "pdf_feature", "feature_pdf"),
            ]
            cols = st.columns(2, gap="medium")
            for idx, (label, page, key) in enumerate(cards):
                with cols[idx % 2]:
                    if st.button(label, key="launch_" + page, use_container_width=True):
                        st.session_state.current_page = page
                        st.rerun()
            st.write("")
            st.caption("Your original AI Chat and Maths Tutor remain available from the AI home page.")
            if st.button("← Back to AI Home", key="feature_hub_home"):
                st.session_state.current_page = "home"
                st.rerun()
        st.stop()

    # 1. VOICE CONVERSATION
    if st.session_state.current_page == "voice_feature":
        with st.container(key="feature_voice"):
            _feature_go_home()
            st.markdown('<div class="feature-title">Voice Conversation</div><div class="feature-subtitle">Speak naturally · hear the response</div>', unsafe_allow_html=True)
            st.markdown('<div class="feature-copy">Record a voice message, send it to the AI, and listen to the reply using your browser’s speech voice.</div>', unsafe_allow_html=True)
            voice_audio = st.audio_input("Record your message", key="feature_voice_audio")
            voice_extra = st.text_input("Optional context", placeholder="Add a little context (optional)", key="feature_voice_context")
            if st.button("🎧 Start conversation", key="feature_voice_send", use_container_width=True, disabled=voice_audio is None):
                client = _feature_groq_client()
                if client:
                    try:
                        with st.spinner("Transcribing your voice..."):
                            transcript = client.audio.transcriptions.create(
                                file=("voice.wav", voice_audio.getvalue()),
                                model=WHISPER_MODEL,
                                response_format="text",
                            )
                        spoken_text = str(transcript).strip()
                        st.markdown("**You said:**")
                        st.info(spoken_text or "No clear speech was detected.")
                        if spoken_text:
                            prompt = (voice_extra.strip() + "\n\n" if voice_extra.strip() else "") + spoken_text
                            with st.spinner("Preparing your spoken reply..."):
                                answer = _feature_ai_text(client, prompt, "You are KASHAN'S AI in a friendly voice conversation. Reply naturally, clearly, and concisely. Reply in the language the user speaks.", 1600)
                            st.markdown("**KASHAN'S AI:**")
                            st.markdown(answer)
                            safe_answer = json.dumps(answer, ensure_ascii=True).replace("</", "<\\/")
                            components.html(f"""
                            <div style="font-family:Arial,sans-serif;color:#17243a;background:#fff;border:1px solid #d6e2ee;border-radius:12px;padding:12px;display:flex;align-items:center;gap:12px;flex-wrap:wrap">
                              <button id="speakReply" type="button" style="border:0;border-radius:9px;padding:10px 16px;background:#315b91;color:#fff;font-weight:700;cursor:pointer">▶ Play AI voice</button>
                              <span id="speechStatus" role="status" style="font-size:13px;color:#334155">Tap to hear the reply. Browser voice support is required.</span>
                            </div>
                            <script>
                            (() => {{
                              const text = {safe_answer};
                              const button = document.getElementById("speakReply");
                              const status = document.getElementById("speechStatus");
                              if (!("speechSynthesis" in window) || !("SpeechSynthesisUtterance" in window)) {{
                                button.disabled = true;
                                status.textContent = "Speech playback is not supported in this browser.";
                                return;
                              }}
                              function languageFor(value) {{
                                if (/[\\u0600-\\u06FF]/.test(value)) return "ur-PK";
                                if (/[\\u0900-\\u097F]/.test(value)) return "hi-IN";
                                if (/[\\u0980-\\u09FF]/.test(value)) return "bn-BD";
                                if (/[\\u4E00-\\u9FFF]/.test(value)) return "zh-CN";
                                if (/[\\u3040-\\u30FF]/.test(value)) return "ja-JP";
                                return "en-US";
                              }}
                              button.addEventListener("click", () => {{
                                try {{
                                  window.speechSynthesis.cancel();
                                  const utterance = new SpeechSynthesisUtterance(text);
                                  const wanted = languageFor(text);
                                  utterance.lang = wanted;
                                  utterance.rate = 0.96;
                                  const voices = window.speechSynthesis.getVoices();
                                  const match = voices.find(v => v.lang && v.lang.toLowerCase() === wanted.toLowerCase())
                                    || voices.find(v => v.lang && v.lang.toLowerCase().startsWith(wanted.slice(0,2).toLowerCase()));
                                  if (match) utterance.voice = match;
                                  utterance.onstart = () => status.textContent = "Speaking…";
                                  utterance.onend = () => status.textContent = "Playback finished. Tap again to replay.";
                                  utterance.onerror = () => status.textContent = "Playback failed. Check browser/device speech settings.";
                                  window.speechSynthesis.speak(utterance);
                                  if (!match) status.textContent = "Using the browser's default voice for " + wanted + ".";
                                }} catch (error) {{
                                  status.textContent = "Could not start speech playback in this browser.";
                                }}
                              }});
                            }})();
                            </script>
                            """, height=88, scrolling=False)
                    except Exception as error:
                        st.error(f"Voice conversation error: {type(error).__name__}: {error}")
            st.caption("Speech playback depends on the browser/device. This tool uses Groq Whisper for transcription.")
        st.stop()

    # 2. LIVE WEB SEARCH
    if st.session_state.current_page == "search_feature":
        with st.container(key="feature_search"):
            _feature_go_home()
            st.markdown('<div class="feature-title">Live Web Search</div><div class="feature-subtitle">Find · verify · understand</div>', unsafe_allow_html=True)
            st.markdown('<div class="feature-copy">Search the web for recent information, then let KASHAN’S AI summarize the results with source links.</div>', unsafe_allow_html=True)
            search_query = st.text_input("What should I search for?", placeholder="e.g. Latest technology news", key="feature_web_query")
            search_count = st.select_slider("Number of results", options=[3, 5, 8], value=5, key="feature_web_count")
            if st.button("🌐 Search the web", key="feature_web_run", use_container_width=True, disabled=not search_query.strip()):
                st.session_state.feature_web_results = []
                st.session_state.feature_web_query_saved = search_query.strip()
                try:
                    try:
                        from ddgs import DDGS
                    except ImportError:
                        # Compatibility with deployments still using the older package name.
                        from duckduckgo_search import DDGS
                    with st.spinner("Searching the web..."):
                        web_results = list(DDGS().text(search_query.strip(), max_results=int(search_count)))
                    if not web_results:
                        st.session_state.feature_web_results = []
                        st.session_state.feature_web_query_saved = search_query.strip()
                        st.warning("No search results were returned. Try a more specific query.")
                    else:
                        st.session_state.feature_web_results = web_results
                        st.session_state.feature_web_query_saved = search_query.strip()
                except ImportError:
                    st.error("Live search dependency is missing. Install `ddgs` (recommended) in the app environment.")
                except Exception as error:
                    st.error(f"Web search failed: {type(error).__name__}: {error}")
            results = st.session_state.get("feature_web_results", [])
            if results:
                st.markdown("### Search results")
                for number, item in enumerate(results, 1):
                    title = item.get("title") or f"Result {number}"
                    body = item.get("body") or item.get("snippet") or ""
                    href = item.get("href") or item.get("url") or ""
                    st.markdown(f"**{number}. [{title}]({href})**" if href else f"**{number}. {title}**")
                    st.write(body)
                    st.divider()
                if st.button("✨ Summarize these results with AI", key="feature_web_summarize"):
                    client = _feature_groq_client()
                    if client:
                        context = "\n\n".join(f"Title: {r.get('title','')}\nURL: {r.get('href','')}\nSummary: {r.get('body','')}" for r in results)
                        try:
                            with st.spinner("Summarizing sources..."):
                                summary = _feature_ai_text(client, f"Search query: {st.session_state.get('feature_web_query_saved','')}\n\nSearch results:\n{context}\n\nSummarize the findings. Distinguish facts from uncertainty and cite the supplied URLs inline.", "You are a careful research assistant. Do not invent facts or sources.", 2200)
                            st.markdown("### AI research summary")
                            st.markdown(summary)
                        except Exception as error:
                            st.error(f"Summary error: {type(error).__name__}: {error}")
        st.stop()

    # 3. IMAGE UNDERSTANDING
    if st.session_state.current_page == "image_feature":
        with st.container(key="feature_image"):
            _feature_go_home()
            st.markdown('<div class="feature-title">Image Understanding</div><div class="feature-subtitle">Upload · ask · explore</div>', unsafe_allow_html=True)
            st.markdown('<div class="feature-copy">Upload an image and ask questions about what is visible. The original vision model configuration is reused.</div>', unsafe_allow_html=True)
            image_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg", "webp"], key="feature_image_upload")
            image_question = st.text_area("What would you like to know?", value="Describe this image and explain its important details.", key="feature_image_question", height=100)
            if image_file:
                st.image(image_file, caption=image_file.name, use_container_width=True)
            if st.button("🪄 Understand image", key="feature_image_run", use_container_width=True, disabled=image_file is None):
                client = _feature_groq_client()
                if client:
                    try:
                        image_obj = Image.open(image_file).convert("RGB")
                        image_obj.thumbnail((1400, 1400))
                        buffer = io.BytesIO()
                        image_obj.save(buffer, format="JPEG", quality=88)
                        encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
                        with st.spinner("Looking at the image..."):
                            vision_result = client.chat.completions.create(
                                model=VISION_MODEL,
                                messages=[{"role":"user","content":[{"type":"text","text":image_question.strip() or "Describe this image."},{"type":"image_url","image_url":{"url":"data:image/jpeg;base64," + encoded}}]}],
                                max_tokens=1800,
                            )
                        st.markdown("### Image analysis")
                        st.markdown(vision_result.choices[0].message.content or "No description returned.")
                    except Exception as error:
                        st.error(f"Image understanding error: {type(error).__name__}: {error}")
        st.stop()

    # 4. PRESENTATION MAKER
    if st.session_state.current_page == "presentation_feature":
        with st.container(key="feature_presentation"):
            _feature_go_home()
            st.markdown('<div class="feature-title">Presentation Maker</div><div class="feature-subtitle">Turn an idea into slides</div>', unsafe_allow_html=True)
            st.markdown('<div class="feature-copy">Create a presentation outline with AI and export it as an editable PowerPoint file.</div>', unsafe_allow_html=True)
            deck_topic = st.text_input("Presentation topic", placeholder="e.g. Renewable energy", key="feature_ppt_topic")
            deck_audience = st.selectbox("Audience", ["School / college", "Professional", "General audience", "Beginner learners"], key="feature_ppt_audience")
            deck_slides = st.slider("Number of slides", 4, 12, 7, key="feature_ppt_slides")
            deck_style = st.selectbox("Visual style", ["Modern minimal", "Elegant dark", "Bright educational", "Professional corporate"], key="feature_ppt_style")
            if st.button("✨ Generate PowerPoint", key="feature_ppt_generate", use_container_width=True, disabled=not deck_topic.strip()):
                # Never leave an older deck presented as the result of a failed new request.
                st.session_state.pop("feature_ppt_bytes", None)
                st.session_state.pop("feature_ppt_name", None)
                st.session_state.pop("feature_ppt_outline", None)
                client = _feature_groq_client()
                if client:
                    try:
                        prompt = f"Create a {deck_slides}-slide presentation about: {deck_topic}. Audience: {deck_audience}. Style: {deck_style}. Output exactly one title line beginning 'TITLE:' then for each slide a line 'SLIDE: Slide title' followed by 3-5 concise bullet lines beginning '- '. Include a useful opening and conclusion. No markdown tables."
                        with st.spinner("Designing your slides..."):
                            outline = _feature_ai_text(client, prompt, "You are an expert presentation designer. Be accurate, structured, and concise. Return exactly the requested number of slide sections, with each section using the required SLIDE: heading and 3-5 bullet lines.", 4500)
                        from pptx import Presentation
                        from pptx.util import Inches, Pt
                        from pptx.dml.color import RGBColor
                        prs = Presentation()
                        prs.slide_width = Inches(13.333)
                        prs.slide_height = Inches(7.5)
                        # Apply an intentional, readable palette to every slide.
                        palettes = {
                            "Modern minimal": ((20, 35, 58), (244, 248, 252), (49, 93, 139)),
                            "Elegant dark": ((25, 24, 48), (247, 244, 255), (171, 139, 226)),
                            "Bright educational": ((255, 250, 230), (34, 47, 72), (226, 145, 45)),
                            "Professional corporate": ((239, 245, 250), (29, 48, 69), (35, 111, 137)),
                        }
                        bg_rgb, ink_rgb, accent_rgb = palettes.get(deck_style, palettes["Modern minimal"])
                        lines = [line.strip() for line in outline.splitlines() if line.strip()]
                        title_text = deck_topic.strip()
                        for line in lines:
                            if line.upper().startswith("TITLE:"):
                                title_text = line.split(":",1)[1].strip() or title_text
                                break
                        title_slide = prs.slides.add_slide(prs.slide_layouts[0])
                        title_fill = title_slide.background.fill
                        title_fill.solid()
                        title_fill.fore_color.rgb = RGBColor(*bg_rgb)
                        title_slide.shapes.title.text = title_text
                        title_slide.shapes.title.text_frame.paragraphs[0].font.color.rgb = RGBColor(*ink_rgb)
                        title_slide.shapes.title.text_frame.paragraphs[0].font.size = Pt(34)
                        title_slide.placeholders[1].text = f"Prepared for {deck_audience} · {deck_style}"
                        for paragraph in title_slide.placeholders[1].text_frame.paragraphs:
                            paragraph.font.color.rgb = RGBColor(*accent_rgb)
                            paragraph.font.size = Pt(18)
                        slide_data = []
                        current = None
                        for line in lines:
                            slide_heading = re.match(r"^SLIDE(?:\s+\d+)?\s*:\s*(.+)$", line, flags=re.IGNORECASE)
                            bullet_match = re.match(r"^(?:[-•*]|\d+[.)])\s+(.+)$", line)
                            if slide_heading:
                                if current:
                                    slide_data.append(current)
                                current = [slide_heading.group(1).strip(), []]
                            elif current and bullet_match:
                                current[1].append(bullet_match.group(1).strip())
                        if current:
                            slide_data.append(current)
                        if not slide_data:
                            slide_data = [(f"Key idea {i+1}", [x.strip("-•* ") for x in lines if x.startswith(("-", "•", "*"))][i*4:(i+1)*4]) for i in range(max(1, min(deck_slides-1, 5)))]
                        expected_content_slides = deck_slides - 1
                        if len(slide_data) < expected_content_slides:
                            st.warning(f"The AI returned {len(slide_data)} content slides; {expected_content_slides} were requested. The PowerPoint will include the content that was successfully generated.")
                        for slide_title, bullets in slide_data[:expected_content_slides]:
                            slide = prs.slides.add_slide(prs.slide_layouts[1])
                            slide_fill = slide.background.fill
                            slide_fill.solid()
                            slide_fill.fore_color.rgb = RGBColor(*bg_rgb)
                            slide.shapes.title.text = slide_title
                            for paragraph in slide.shapes.title.text_frame.paragraphs:
                                paragraph.font.color.rgb = RGBColor(*ink_rgb)
                                paragraph.font.size = Pt(28)
                            tf = slide.placeholders[1].text_frame
                            tf.clear()
                            for idx, bullet in enumerate((bullets or ["Explore the key ideas and supporting details."])[:6]):
                                para = tf.paragraphs[0] if idx == 0 else tf.add_paragraph()
                                para.text = bullet
                                para.level = 0
                                para.font.size = Pt(21)
                                para.font.color.rgb = RGBColor(*ink_rgb)
                        ppt_buffer = io.BytesIO()
                        prs.save(ppt_buffer)
                        st.session_state.feature_ppt_bytes = ppt_buffer.getvalue()
                        st.session_state.feature_ppt_name = "AI_Presentation_" + re.sub(r"[^A-Za-z0-9_-]+", "_", deck_topic.strip())[:45] + ".pptx"
                        st.session_state.feature_ppt_outline = outline
                    except ImportError:
                        st.error("PowerPoint export dependency missing. Install python-pptx from requirements.txt.")
                    except Exception as error:
                        st.error(f"Presentation generation error: {type(error).__name__}: {error}")
            if st.session_state.get("feature_ppt_bytes"):
                st.markdown("### Your presentation is ready")
                st.download_button("⬇️ Download PowerPoint", data=st.session_state.feature_ppt_bytes, file_name=st.session_state.get("feature_ppt_name", "AI_Presentation.pptx"), mime="application/vnd.openxmlformats-officedocument.presentationml.presentation", key="feature_ppt_download", use_container_width=True)
                with st.expander("Preview generated slide outline"):
                    st.markdown(st.session_state.get("feature_ppt_outline", ""))
        st.stop()

    # 5. DATA ANALYST
    if st.session_state.current_page == "data_feature":
        with st.container(key="feature_data"):
            _feature_go_home()
            st.markdown('<div class="feature-title">Data Analyst</div><div class="feature-subtitle">Explore · calculate · discover</div>', unsafe_allow_html=True)
            st.markdown('<div class="feature-copy">Upload a CSV or Excel sheet to preview data, view basic statistics, and ask AI to explain patterns.</div>', unsafe_allow_html=True)
            data_file = st.file_uploader("Upload CSV or Excel", type=["csv", "xlsx", "xls"], key="feature_data_upload")
            data_question = st.text_area("What would you like to find out?", value="Summarize this dataset and point out useful patterns.", key="feature_data_question", height=95)
            if data_file:
                try:
                    import pandas as pd
                    file_bytes = data_file.getvalue()
                    if data_file.name.lower().endswith(".csv"):
                        dataframe = None
                        for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
                            try:
                                dataframe = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding, low_memory=False)
                                break
                            except UnicodeDecodeError:
                                continue
                        if dataframe is None:
                            raise ValueError("CSV text encoding could not be detected. Please save it as UTF-8 and upload again.")
                    else:
                        dataframe = pd.read_excel(io.BytesIO(file_bytes))
                    if len(dataframe.columns) == 0:
                        raise ValueError("This file has no readable columns. Check the file format and try again.")
                    if dataframe.empty:
                        st.warning("The file has column headers but no data rows. Add data rows and upload it again for analysis.")
                    st.markdown("### Dataset preview")
                    st.dataframe(dataframe.head(30), use_container_width=True)
                    st.caption(f"{len(dataframe):,} rows · {len(dataframe.columns):,} columns")
                    numeric = dataframe.select_dtypes(include="number")
                    if not numeric.empty:
                        st.markdown("### Numeric overview")
                        st.dataframe(numeric.describe().round(2), use_container_width=True)
                        chart_column = st.selectbox("Quick chart column", list(numeric.columns), key="feature_data_chart_col")
                        st.bar_chart(dataframe[chart_column].dropna().head(100))
                    if st.button("📈 Analyze with AI", key="feature_data_analyze", use_container_width=True, disabled=dataframe.empty):
                        client = _feature_groq_client()
                        if client:
                            try:
                                profile = dataframe.describe(include="all").to_string(max_rows=25, max_cols=15)
                                missing = dataframe.isna().sum().sort_values(ascending=False).head(20).to_string()
                                duplicate_rows = int(dataframe.duplicated().sum())
                                numeric = dataframe.select_dtypes(include="number")
                                correlations = ""
                                if len(numeric.columns) >= 2:
                                    correlations = numeric.corr().round(3).iloc[:12, :12].to_string()
                                categorical_sections = []
                                for column in dataframe.select_dtypes(exclude="number").columns[:8]:
                                    top_values = dataframe[column].astype("string").value_counts(dropna=False).head(5).to_string()
                                    categorical_sections.append(f"{column}:\n{top_values}")
                                categorical_profile = "\n\n".join(categorical_sections) or "No categorical columns."
                                sample = dataframe.head(15).iloc[:, :30].to_csv(index=False)
                                column_types = dataframe.dtypes.iloc[:40].to_string()
                                omitted_columns = max(0, len(dataframe.columns) - 30)
                                prompt = (
                                    f"User question: {data_question}\n"
                                    f"Dataset shape: {dataframe.shape[0]} rows x {dataframe.shape[1]} columns\n"
                                    f"Column types (first 40):\n{column_types}\n"
                                    f"Columns omitted from the row sample: {omitted_columns}\n"
                                    f"Descriptive statistics (computed from the full dataset):\n{profile}\n"
                                    f"Missing values by column (top 20):\n{missing}\n"
                                    f"Duplicate rows: {duplicate_rows}\n"
                                    f"Numeric correlations (computed where possible):\n{correlations or 'Not enough numeric columns.'}\n"
                                    f"Common categorical values:\n{categorical_profile}\n"
                                    f"Sample rows (first 15 only):\n{sample}\n"
                                    "Analyze only the supplied evidence. Distinguish full-dataset computed statistics from sample-based observations. "
                                    "Do not claim to have inspected every row individually. State uncertainty, explain relevant limitations, "
                                    "and give concrete findings that answer the user's question."
                                )
                                with st.spinner("Analyzing computed dataset statistics..."):
                                    analysis = _feature_ai_text(client, prompt, "You are a careful data analyst. Interpret only the supplied data and statistics. Separate observations from hypotheses.", 2800)
                                st.markdown("### AI analysis")
                                st.markdown(analysis)
                            except Exception as error:
                                st.error(f"Data analysis error: {type(error).__name__}: {error}")
                except Exception as error:
                    st.error(f"Could not read this dataset: {type(error).__name__}: {error}")
        st.stop()

    # 6. PDF EXPERT
    if st.session_state.current_page == "pdf_feature":
        with st.container(key="feature_pdf"):
            _feature_go_home()
            st.markdown('<div class="feature-title">PDF Expert</div><div class="feature-subtitle">Read · question · summarize</div>', unsafe_allow_html=True)
            st.markdown('<div class="feature-copy">Upload a PDF, extract its text, ask questions, or request a structured summary.</div>', unsafe_allow_html=True)
            pdf_file = st.file_uploader("Upload a PDF document", type=["pdf"], key="feature_pdf_upload")
            pdf_question = st.text_area("Ask about this PDF", value="Summarize this document in clear sections and list its key points.", key="feature_pdf_question", height=100)
            if pdf_file:
                try:
                    pdf_reader = PdfReader(pdf_file)
                    page_count = len(pdf_reader.pages)
                    pdf_text = "\n\n".join(f"Page {idx+1}: {page.extract_text() or ''}" for idx, page in enumerate(pdf_reader.pages))
                    st.caption(f"{pdf_file.name} · {page_count} pages · {len(pdf_text):,} extracted characters")
                    with st.expander("Preview extracted text"):
                        st.text(pdf_text[:12000] or "No selectable text was found. This may be a scanned PDF.")
                    if st.button("📚 Ask PDF Expert", key="feature_pdf_ask", use_container_width=True):
                        client = _feature_groq_client()
                        if client:
                            if not pdf_text.strip():
                                st.warning("No selectable text was found. This PDF may contain scanned pages and need OCR.")
                            else:
                                try:
                                    # Keep the prompt bounded to avoid oversized API requests.
                                    bounded_text = pdf_text[:42000]
                                    if len(pdf_text) > len(bounded_text):
                                        st.warning("This PDF contains more text than can fit in one AI request. The first 42,000 characters are being analyzed; later pages may not be included.")
                                    prompt = f"PDF filename: {pdf_file.name}\nQuestion: {pdf_question}\n\nExtracted PDF text (may be truncated):\n{bounded_text}\n\nAnswer using only this supplied document text. If the answer is not present in the supplied portion, say so. Refer to page numbers when possible and never imply that omitted text was reviewed."
                                    with st.spinner("Reading your PDF..."):
                                        pdf_answer = _feature_ai_text(client, prompt, "You are a precise document analyst. Ground every claim in the supplied PDF text. Never invent document contents.", 2600)
                                    st.markdown("### PDF Expert response")
                                    st.markdown(pdf_answer)
                                except Exception as error:
                                    st.error(f"PDF analysis error: {type(error).__name__}: {error}")
                except Exception as error:
                    st.error(f"Could not read this PDF: {type(error).__name__}: {error}")
        st.stop()


    # ============================================================
    # MATHS TUTOR PAGE
    # ============================================================

    if st.session_state.current_page == "maths_tutor":
        with st.container(key="maths_tutor_shell"):
            back_col, empty_col = st.columns([1.1, 4.9])
            with back_col:
                if st.button("← Home", key="maths_tutor_back", use_container_width=True):
                    st.session_state.current_page = "home"
                    st.rerun()

            st.markdown("""
            <div class="maths-tutor-title">Maths Tutor</div>
            <div class="maths-tutor-subtitle">ASK · SOLVE · UNDERSTAND</div>
            """, unsafe_allow_html=True)

            st.markdown(
                "Ask a maths question and I will solve it with clear, manageable steps."
            )

            try:
                tutor_client = Groq(api_key=st.secrets["GROQ_API_KEY"])
            except Exception:
                st.error("AI connection failed. Check Streamlit Secrets.")
                st.stop()

            for tutor_message in st.session_state.maths_tutor_messages:
                with st.chat_message(tutor_message["role"]):
                    st.markdown(tutor_message["content"])

            maths_question = st.chat_input(
                "Type your maths question here...",
                key="maths_tutor_input"
            )

            if maths_question and maths_question.strip():
                question = maths_question.strip()
                st.session_state.maths_tutor_messages.append({
                    "role": "user",
                    "content": question
                })

                with st.chat_message("user"):
                    st.markdown(question)

                maths_system_prompt = """You are KASHAN'S AI Maths Tutor.
    Your job is to solve the student's mathematics question and teach the method clearly.

    Rules:
    - Solve the exact question asked. Check arithmetic and algebra carefully.
    - Explain in short, numbered steps. Show the necessary formula and substitution.
    - Keep the explanation concise and do not go unnecessarily far beyond the question.
    - Give the final answer clearly at the end.
    - If a question has more than one valid method, use the simplest suitable method.
    - If information is missing or the question is unclear, ask only for the missing detail.
    - Use readable mathematical notation and explain symbols briefly when needed.
    - Reply in the language used by the student; Roman Urdu is welcome when the student uses it.
    - Do not invent values or skip an important calculation step.
    """

                tutor_history = [{"role": "system", "content": maths_system_prompt}]
                tutor_history.extend(st.session_state.maths_tutor_messages[:-1])
                tutor_history.append({"role": "user", "content": question})

                try:
                    with st.chat_message("assistant"):
                        with st.spinner("Solving your question..."):
                            tutor_result = tutor_client.chat.completions.create(
                                model=CHAT_MODEL,
                                messages=tutor_history,
                                temperature=0.2,
                                max_tokens=1400
                            )
                            tutor_answer = tutor_result.choices[0].message.content or "I could not produce an answer. Please try asking the question another way."
                            st.markdown(tutor_answer)

                    st.session_state.maths_tutor_messages.append({
                        "role": "assistant",
                        "content": tutor_answer
                    })
                except Exception as error:
                    st.error(f"Maths Tutor error: {type(error).__name__}: {error}")

            # Keep the Maths Tutor positioned at the newest message while preserving manual upward scrolling.
            st.components.v1.html("""
            <script>
            (() => {
                const scrollToLatestTutorMessage = () => {
                    try {
                        const doc = window.parent.document;
                        const shell = doc.querySelector('.st-key-maths_tutor_shell');
                        if (!shell) return;
                        const messages = shell.querySelectorAll('[data-testid="stChatMessage"]');
                        if (messages.length) {
                            messages[messages.length - 1].scrollIntoView({
                                behavior: 'smooth',
                                block: 'end'
                            });
                        }
                    } catch (error) {
                        // Scrolling is an enhancement; the tutor remains usable if the browser blocks it.
                    }
                };
                requestAnimationFrame(() => requestAnimationFrame(scrollToLatestTutorMessage));
            })();
            </script>
            """, height=0, scrolling=False)

        st.stop()


    # ============================================================
    # AI CHAT PAGE
    # ============================================================

    if st.session_state.current_page == "chat":

        st.markdown("""
        <div class="chat-snow-layer" aria-hidden="true">
            <span class="chat-snowflake" style="left:3%;--flake-size:4px;--fall-duration:12s;--fall-delay:-3s"></span>
            <span class="chat-snowflake" style="left:8%;--flake-size:7px;--fall-duration:16s;--fall-delay:-11s"></span>
            <span class="chat-snowflake" style="left:14%;--flake-size:3px;--fall-duration:10s;--fall-delay:-5s"></span>
            <span class="chat-snowflake" style="left:20%;--flake-size:6px;--fall-duration:14s;--fall-delay:-8s"></span>
            <span class="chat-snowflake" style="left:27%;--flake-size:4px;--fall-duration:11s;--fall-delay:-1s"></span>
            <span class="chat-snowflake" style="left:33%;--flake-size:8px;--fall-duration:18s;--fall-delay:-13s"></span>
            <span class="chat-snowflake" style="left:39%;--flake-size:3px;--fall-duration:13s;--fall-delay:-7s"></span>
            <span class="chat-snowflake" style="left:45%;--flake-size:5px;--fall-duration:15s;--fall-delay:-4s"></span>
            <span class="chat-snowflake" style="left:52%;--flake-size:4px;--fall-duration:12s;--fall-delay:-10s"></span>
            <span class="chat-snowflake" style="left:58%;--flake-size:7px;--fall-duration:17s;--fall-delay:-6s"></span>
            <span class="chat-snowflake" style="left:64%;--flake-size:3px;--fall-duration:11s;--fall-delay:-2s"></span>
            <span class="chat-snowflake" style="left:70%;--flake-size:6px;--fall-duration:15s;--fall-delay:-12s"></span>
            <span class="chat-snowflake" style="left:76%;--flake-size:4px;--fall-duration:13s;--fall-delay:-9s"></span>
            <span class="chat-snowflake" style="left:82%;--flake-size:8px;--fall-duration:19s;--fall-delay:-5s"></span>
            <span class="chat-snowflake" style="left:88%;--flake-size:3px;--fall-duration:10s;--fall-delay:-7s"></span>
            <span class="chat-snowflake" style="left:94%;--flake-size:5px;--fall-duration:14s;--fall-delay:-14s"></span>
            <span class="chat-snowflake" style="left:98%;--flake-size:4px;--fall-duration:16s;--fall-delay:-1s"></span>
        </div>
        """, unsafe_allow_html=True)

        top_left, top_space = st.columns([1, 5])

        with top_left:
            if st.button(
                "← Home",
                key="chat_home_button",
                use_container_width=True
            ):
                st.session_state.current_page = "home"
                st.rerun()

        st.markdown("""
        <div class="hero">
            <div class="logo">✦</div>
            <div class="brand">KASHAN'S AI</div>
            <div class="subtitle">YOUR INTELLIGENT AI ASSISTANT</div>
        </div>
        """, unsafe_allow_html=True)


        # --------------------------------------------------------
        # GROQ CONNECTION - ORIGINAL CONFIGURATION PRESERVED
        # --------------------------------------------------------

        try:
            client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        except Exception:
            st.error("AI connection failed. Check Streamlit Secrets.")
            st.stop()


        # --------------------------------------------------------
        # SIDEBAR
        # --------------------------------------------------------

        with st.sidebar:
            st.markdown("## ✦ KASHAN'S AI")
            st.caption("Your personal AI assistant")
            st.markdown("**Created by Kashan King 👑**")

            st.divider()

            if st.button("＋ New chat", use_container_width=True):
                st.session_state.messages = []
                st.session_state.last_answer = ""
                st.rerun()

            if st.button("Clear history", use_container_width=True):
                st.session_state.messages = []
                st.session_state.last_answer = ""
                st.rerun()

            st.divider()

            if st.button("← AI Home", use_container_width=True):
                st.session_state.current_page = "home"
                st.rerun()


        # --------------------------------------------------------
        # CHAT HISTORY
        # --------------------------------------------------------

        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])


        # --------------------------------------------------------
        # CHAT INPUT - ORIGINAL OPTIONS PRESERVED
        # --------------------------------------------------------

        # Streamlit versions differ in their chat_input audio support. Prefer the
        # integrated audio control, and provide a separate recorder fallback when
        # the installed version does not accept the audio arguments.
        chat_audio_fallback = None
        chat_audio_fallback_send = False
        try:
            submission = st.chat_input(
                "Message KASHAN'S AI...",
                accept_file="multiple",
                file_type=["png", "jpg", "jpeg", "webp", "pdf"],
                accept_audio=True,
                audio_sample_rate=16000,
                max_upload_size=20,
                key="nexora_chat"
            )
        except TypeError:
            st.caption("Your installed Streamlit version uses the separate microphone control below.")
            chat_audio_fallback = st.audio_input("Record a voice message", key="chat_voice_fallback")
            chat_audio_fallback_send = st.button(
                "🎙️ Send voice message",
                key="chat_voice_fallback_send",
                use_container_width=True,
                disabled=chat_audio_fallback is None,
            )
            submission = st.chat_input(
                "Message KASHAN'S AI...",
                accept_file="multiple",
                file_type=["png", "jpg", "jpeg", "webp", "pdf"],
                max_upload_size=20,
                key="nexora_chat_fallback"
            )
        st.caption("Voice input works through your browser microphone permission. On a laptop, allow microphone access for this site before recording.")


        # --------------------------------------------------------
        # PROCESS SUBMISSION
        # --------------------------------------------------------

        if submission or chat_audio_fallback_send:

            user_text = (getattr(submission, "text", "") or "") if submission else ""
            files = (getattr(submission, "files", None) or []) if submission else []
            audio = (getattr(submission, "audio", None) if submission else None)
            if audio is None and chat_audio_fallback_send:
                audio = chat_audio_fallback

            # Voice transcription
            if audio:
                try:
                    transcript = client.audio.transcriptions.create(
                        file=("voice.wav", audio.getvalue()),
                        model=WHISPER_MODEL,
                        response_format="text"
                    )
                    transcript_text = str(transcript).strip()
                    if not transcript_text:
                        st.error("No clear speech was detected. Please try recording again in a quiet place.")
                        st.stop()
                    user_text += "\n" + transcript_text
                except Exception as e:
                    st.error(f"Voice transcription failed: {e}")
                    st.stop()

            image_parts = []
            pdf_parts = []

            # Process attachments
            for uploaded in files:

                file_name = uploaded.name.lower()

                if file_name.endswith(".pdf"):
                    try:
                        reader = PdfReader(uploaded)
                        extracted = "\n".join(
                            page.extract_text() or ""
                            for page in reader.pages
                        )
                        if not extracted.strip():
                            st.warning(f"No selectable text was found in {uploaded.name}. Scanned PDFs need OCR before AI Chat can read their contents.")
                        else:
                            if len(extracted) > 25000:
                                st.warning(f"{uploaded.name}: only the first 25,000 extracted characters will be included in this chat request.")
                            pdf_parts.append(
                                f"PDF: {uploaded.name}\n{extracted[:25000]}"
                            )
                    except Exception:
                        st.warning(f"Could not read {uploaded.name}")

                elif file_name.endswith((".png", ".jpg", ".jpeg", ".webp")):
                    try:
                        image = Image.open(uploaded).convert("RGB")
                        image.thumbnail((1200, 1200))

                        buffer = io.BytesIO()
                        image.save(buffer, format="JPEG", quality=85)

                        encoded = base64.b64encode(
                            buffer.getvalue()
                        ).decode("utf-8")

                        image_parts.append(encoded)

                    except Exception:
                        st.warning(f"Could not open {uploaded.name}")

            if pdf_parts:
                user_text += "\n\nUploaded document content:\n"
                user_text += "\n\n".join(pdf_parts)

            if not user_text.strip() and not image_parts:
                user_text = "Please analyze the attached file."

            # Display user message
            st.session_state.messages.append({
                "role": "user",
                "content": user_text
            })

            with st.chat_message("user"):
                st.markdown(user_text or "Please analyze the attachment.")

                for encoded in image_parts:
                    st.image(
                        base64.b64decode(encoded),
                        width=220
                    )

                for uploaded in files:
                    if uploaded.name.lower().endswith(".pdf"):
                        st.caption("📄 " + uploaded.name)

                if audio:
                    st.caption("🎙️ Voice message received")

            # Generate answer
            try:
                with st.chat_message("assistant"):
                    with st.spinner("KASHAN'S AI is thinking..."):

                        history = [
                            {"role": "system", "content": SYSTEM_PROMPT}
                        ]

                        history.extend(st.session_state.messages[:-1])

                        if image_parts:
                            content = [
                                {
                                    "type": "text",
                                    "text": user_text or "Describe this image."
                                }
                            ]

                            for encoded in image_parts:
                                content.append({
                                    "type": "image_url",
                                    "image_url": {
                                        "url": "data:image/jpeg;base64," + encoded
                                    }
                                })

                            history.append({
                                "role": "user",
                                "content": content
                            })

                            result = client.chat.completions.create(
                                model=VISION_MODEL,
                                messages=history,
                                max_tokens=2048
                            )

                        else:
                            history.append({
                                "role": "user",
                                "content": user_text
                            })

                            result = client.chat.completions.create(
                                model=CHAT_MODEL,
                                messages=history,
                                temperature=0.7,
                                max_tokens=2048
                            )

                        answer = result.choices[0].message.content or ""
                        st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

                st.session_state.last_answer = answer

            except Exception as e:
                st.error(f"AI Error: {type(e).__name__}: {e}")


        # --------------------------------------------------------
        # FOOTER
        # --------------------------------------------------------

        st.markdown("""
        <div class="footer">
            KASHAN'S AI · Created by
            <span style="color:#E9C47A;">Kashan King 👑</span>
        </div>
        """, unsafe_allow_html=True)

else:
    _component_value = mobile_component(key="mobile_app_main_component", default=None)
    if isinstance(_component_value, dict) and _component_value.get("type") == "open_my_ai":
        st.session_state.show_my_ai = True
        st.rerun()
