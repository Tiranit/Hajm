import ccxt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import pandas as pd
import mplfinance as mpf
import os
import logging
from datetime import datetime

# -----------------------------
# 🔐 تنظیمات و امنیت
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465

EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

if not all([EMAIL_USER, EMAIL_PASS, EMAIL_TO]):
    raise ValueError("❌ خطا: متغیرهای محیطی EMAIL_USER, EMAIL_PASS, EMAIL_TO تنظیم نشده‌اند!")

exchange = ccxt.mexc()

symbols = ['BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'BNB/USDT', 'SOL/USDT', 'DOGE/USDT', 'TRX/USDT', 'ADA/USDT', 'WBTC/USDT', 'LINK/USDT', 'USDE/USDT', 'XLM/USDT', 'BCH/USDT', 'SUI/USDT', 'AVAX/USDT', 'LTC/USDT', 'HBAR/USDT', 'SHIB/USDT', 'TON/USDT', 'DOT/USDT', 'ZEC/USDT', 'TAO/USDT', 'UNI/USDT', 'WLFI/USDT', 'AAVE/USDT', 'ENA/USDT', 'PEPE/USDT', 'USD1/USDT', 'NEAR/USDT', 'SOL/USDT', 'ETC/USDT', 'APT/USDT', 'ONDO/USDT', 'ASTER/USDT', 'POL/USDT', 'WLD/USDT', 'ARB/USDT', 'ICP/USDT', 'ALGO/USDT', 'ATOM/USDT', 'VET/USDT', 'PUMP/USDT', 'SKY/USDT', 'PAXG/USDT', 'JUP/USDT', 'PENGU/USDT', 'RENDER/USDT', 'SEI/USDT', 'TRUMP/USDT', 'QNT/USDT', 'BONK/USDT', 'FIL/USDT', 'MORPHO/USDT', 'IMX/USDT', 'CAKE/USDT', 'WBTC/USDT', 'TIA/USDT', 'OP/USDT', 'VIRTUAL/USDT', '2Z/USDT', 'INJ/USDT', 'LDO/USDT', 'STX/USDT', 'CRV/USDT', 'FLOKI/USDT', 'XPL/USDT', 'GRT/USDT', 'FET/USDT', 'PYTH/USDT', 'XTZ/USDT', 'KAIA/USDT', 'S/USDT', 'IOTA/USDT', 'ETHFI/USDT', 'CFX/USDT', 'THETA/USDT', 'WIF/USDT', 'PENDLE/USDT', 'TWT/USDT', 'SAND/USDT', 'DASH/USDT', 'STRK/USDT', 'JASMY/USDT', 'GALA/USDT', 'ENS/USDT', 'DOGE/USDT', 'RAY/USDT', 'A/USDT', 'MANA/USDT', 'JTO/USDT', 'FLOW/USDT', 'SYRUP/USDT', 'EIGEN/USDT', 'SUN/USDT', 'SNX/USDT', 'APE/USDT', 'FF/USDT', '0G/USDT', 'DEXE/USDT', 'WAL/USDT', 'COMP/USDT', 'NEO/USDT', 'W/USDT', 'RSR/USDT', 'JST/USDT', 'CHZ/USDT', 'RUNE/USDT', 'XEC/USDT', 'EGLD/USDT', 'DCR/USDT', 'WBTC/USDT', 'KAITO/USDT', 'AXS/USDT', 'DYDX/USDT', 'LUNC/USDT', 'AR/USDT', '1INCH/USDT', 'BAT/USDT', 'BERA/USDT', 'SUPER/USDT', 'GIGGLE/USDT', 'ZK/USDT', 'LINEA/USDT', 'LPT/USDT', 'PLUME/USDT', 'SOL/USDT', 'QTUM/USDT', 'AMP/USDT', 'MOVE/USDT', 'ZEN/USDT', 'AVNT/USDT', 'KMNO/USDT', 'ZRO/USDT', 'SFP/USDT', 'ARKM/USDT', 'TFUEL/USDT', 'CVX/USDT', 'KSM/USDT', 'GLM/USDT', 'SAHARA/USDT', 'PROVE/USDT', 'GAS/USDT', 'PROM/USDT', 'ZRX/USDT', 'TURBO/USDT', 'BIO/USDT', 'YFI/USDT', 'CKB/USDT', 'ZIL/USDT', 'RVN/USDT', 'KAVA/USDT', 'STG/USDT', 'EUL/USDT', 'CELO/USDT', 'BARD/USDT', 'WBTC/USDT', 'ASTR/USDT', 'AWE/USDT', 'T/USDT', 'PNUT/USDT']  # اصلاح اشتباه XPL به XRP
timeframes = ["30m", "1h", "2h", "4h", "1d", "1w"]

limit = 990
VOLUME_FACTOR = 3
MAX_EMAIL_SIZE = 20 * 1024 * 1024  # 20 MB


# -----------------------------
# 📊 بررسی موقعیت‌ها
# -----------------------------
def check_symbol(symbol, timeframe):
    try:
        ohlcv = exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
        if len(ohlcv) < 20:
            return None
        last_20 = ohlcv[-20:]
        highs = [c[2] for c in last_20]
        max_high = max(highs)
        max_index = highs.index(max_high)
        correction_candles = last_20[max_index+1:]
        if len(correction_candles) < 3:
            return None

        correction_volumes = [c[5] for c in correction_candles]
        avg_volume = sum(correction_volumes) / len(correction_volumes)
        heavy_indices = [i for i, v in enumerate(correction_volumes) if v >= VOLUME_FACTOR * avg_volume]
        if not heavy_indices:
            return None

        last_heavy_idx = heavy_indices[-1]
        last_heavy_candle = correction_candles[last_heavy_idx]
        big_volume = last_heavy_candle[5]

        subsequent_candles = correction_candles[last_heavy_idx+1:]
        if len(subsequent_candles) < 4:
            for idx in reversed(heavy_indices[:-1]):
                candidate_candle = correction_candles[idx]
                candidate_volume = candidate_candle[5]
                next_candles = correction_candles[idx+1:]
                if len(next_candles) >= 4 and all(c[5] <= candidate_volume / 3 for c in next_candles):
                    last_heavy_idx = idx
                    big_volume = candidate_volume
                    subsequent_candles = next_candles
                    break
            else:
                return None

        for c in subsequent_candles:
            if c[5] > big_volume / 3:
                return None

        return True

    except Exception as e:
        logging.error(f"{symbol} {timeframe}: {e}")
        return None


# -----------------------------
# 📈 ساخت نمودار
# -----------------------------
def plot_chart(exchange, symbol, timeframe, length):
    try:
        bars = exchange.fetch_ohlcv(symbol, timeframe)
        df = pd.DataFrame(bars, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)
        df_length = df.tail(length)
        os.makedirs('charts', exist_ok=True)
        chart_file = f'charts/{symbol.replace("/", "_")}_{timeframe}_{length}candles.png'
        mpf.plot(df_length, type='candle', volume=True, style='yahoo',
                 savefig=dict(fname=chart_file, dpi=100, bbox_inches="tight"))
        return chart_file
    except Exception as e:
        logging.error(f"Plot error {symbol} {timeframe}: {e}")
        return None


# -----------------------------
# 📬 ارسال ایمیل
# -----------------------------
def send_email(subject, body, images):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_USER
    msg['To'] = EMAIL_TO
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    for img_path in images:
        try:
            with open(img_path, 'rb') as f:
                img = MIMEImage(f.read())
                img.add_header('Content-Disposition', 'attachment', filename=os.path.basename(img_path))
                msg.attach(img)
        except Exception as e:
            logging.warning(f"Cannot attach {img_path}: {e}")

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_USER, EMAIL_PASS)
            server.send_message(msg)
        logging.info(f"📧 ایمیل ارسال شد: {subject}")
    except Exception as e:
        logging.error(f"❌ خطا در ارسال ایمیل: {e}")


# -----------------------------
# 🚀 اجرای اصلی
# -----------------------------
def main():
    results = {}

    for symbol in symbols:
        matched_timeframes = []
        for tf in timeframes:
            if check_symbol(symbol, tf):
                matched_timeframes.append(tf)
        if matched_timeframes:
            ticker = exchange.fetch_ticker(symbol)
            quote_volume = ticker.get('quoteVolume') or 0
            last_price = ticker.get('last') or 0
            volume_usd_24h = quote_volume * last_price
            results[symbol] = {"tfs": matched_timeframes, "volume_usd": volume_usd_24h}

    sorted_results = dict(sorted(results.items(), key=lambda x: x[1]["volume_usd"], reverse=True))
    charts_info = []

    for sym, data in sorted_results.items():
        for tf in data["tfs"]:
            chart_file = plot_chart(exchange, sym, tf, length=limit)
            if chart_file and os.path.exists(chart_file):
                size = os.path.getsize(chart_file)
                charts_info.append((sym, tf, chart_file, size))

    # تقسیم ایمیل‌ها به چند بخش
    batches = []
    current_batch, current_size = [], 0
    for sym, tf, path, size in charts_info:
        if current_size + size > MAX_EMAIL_SIZE and current_batch:
            batches.append(current_batch)
            current_batch, current_size = [], 0
        current_batch.append((sym, tf, path))
        current_size += size
    if current_batch:
        batches.append(current_batch)

    for idx, batch in enumerate(batches, start=1):
        body = f"نتایج موقعیت‌های ترید - تاریخ: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n"
        images = []
        for sym, tf, path in batch:
            ticker = exchange.fetch_ticker(sym)
            quote_volume = ticker.get('quoteVolume') or 0
            last_price = ticker.get('last') or 0
            volume_usd_24h = quote_volume * last_price
            body += f"{sym} | {tf} | 24h Vol: {volume_usd_24h:,.2f} USD\n"
            images.append(path)
        send_email(f"Trade Scanner Report - Part {idx}", body, images)


if __name__ == "__main__":
    main()
