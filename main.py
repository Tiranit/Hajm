import ccxt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import pandas as pd
import mplfinance as mpf
import os

# تنظیمات صرافی و ایمیل
exchange = ccxt.mexc()

symbols = ['BTC/USDT', 'ETH/USDT', 'XPL/USDT', 'SOL/USDT', 'USDE/USDT', 'AVNT/USDT', 'ZKC/USDT', 'XRP/USDT', 'BNB/USDT', 'DOGE/USDT', 'PUMP/USDT', 'AVAX/USDT', 'FORM/USDT', 'SUI/USDT', 'MIRA/USDT', 'ALPINE/USDT', 'KAITO/USDT', 'ADA/USDT', 'BARD/USDT', 'LINEA/USDT', 'LINK/USDT', 'TRX/USDT', 'ENA/USDT', 'COW/USDT', 'WLD/USDT', 'PEPE/USDT', 'PENGU/USDT', '0G/USDT', 'EIGEN/USDT', 'NEAR/USDT', 'LTC/USDT', 'HIFI/USDT', 'ZEC/USDT', 'DOT/USDT', 'PAXG/USDT', 'AAVE/USDT', 'SUN/USDT', 'BERA/USDT', 'SOMI/USDT', 'CRV/USDT', 'ETHFI/USDT', 'SLF/USDT', 'BONK/USDT', 'TRUMP/USDT', 'SEI/USDT', 'ARB/USDT', 'APT/USDT', 'WIF/USDT', 'UNI/USDT', 'HBAR/USDT', 'SKL/USDT', 'SNX/USDT', 'AEVO/USDT', 'S/USDT', 'TAO/USDT', 'ONDO/USDT', 'XLM/USDT', 'TWT/USDT', 'FIDA/USDT', 'W/USDT', 'SHIB/USDT', 'BCH/USDT', 'HOLO/USDT', 'CAKE/USDT', 'TST/USDT', 'USD1/USDT', 'OPEN/USDT', 'HUMA/USDT', 'FET/USDT', 'TON/USDT', 'ZRO/USDT', 'LDO/USDT', 'AWE/USDT', 'FLOKI/USDT', 'POL/USDT', 'PENDLE/USDT', 'ICP/USDT', 'BB/USDT', 'SOLV/USDT', 'FIL/USDT', 'TIA/USDT', 'OM/USDT', 'OP/USDT', 'FTT/USDT', 'ZEN/USDT', 'RENDER/USDT', 'IMX/USDT', 'VIRTUAL/USDT', 'VOXEL/USDT', 'BIO/USDT', 'PLUME/USDT', 'PROVE/USDT', 'TREE/USDT', 'ORDI/USDT', 'RUNE/USDT', 'NEIRO/USDT', 'RLC/USDT', 'DOLO/USDT', 'INJ/USDT', 'REZ/USDT', 'TUT/USDT', 'WBTC/USDT', 'SIGN/USDT', 'KSM/USDT', 'ATOM/USDT', 'SPK/USDT', 'SKY/USDT', 'ETC/USDT', 'VET/USDT', 'ALGO/USDT', 'NMR/USDT', 'RAY/USDT', 'CFX/USDT', 'PNUT/USDT', 'PYTH/USDT', 'YFI/USDT', 'ARKM/USDT', 'ENS/USDT', 'IO/USDT', 'YGG/USDT', 'LISTA/USDT', 'SAND/USDT', 'SYRUP/USDT', 'CTSI/USDT', 'WCT/USDT', 'ALICE/USDT', 'MEME/USDT', 'KAVA/USDT', 'JUP/USDT', 'DYDX/USDT', 'AIXBT/USDT', 'AR/USDT', 'QNT/USDT', 'STRK/USDT', 'APE/USDT', 'RVN/USDT', 'A/USDT', 'SUSHI/USDT', 'MUBARAK/USDT', 'HYPER/USDT', 'RSR/USDT', 'PIXEL/USDT', 'SAHARA/USDT', 'KERNEL/USDT', 'PROM/USDT', 'TRB/USDT', 'INIT/USDT', 'THETA/USDT', 'WOO/USDT', 'EDU/USDT', 'MAV/USDT', 'KMNO/USDT', 'USUAL/USDT', 'JTO/USDT', 'NEO/USDT', 'BOME/USDT', 'VANA/USDT', 'STG/USDT', 'ZK/USDT', 'STX/USDT', 'LA/USDT', 'SSV/USDT', 'C98/USDT', 'PEOPLE/USDT', 'ME/USDT', 'MANA/USDT', 'LQTY/USDT', 'CHZ/USDT', 'LPT/USDT', 'GMX/USDT', 'GRT/USDT', 'C/USDT', 'DEGO/USDT', 'MINA/USDT', 'GPS/USDT', 'AXS/USDT', 'ORCA/USDT', 'A2Z/USDT', 'EGLD/USDT', 'BLUR/USDT', 'ID/USDT', 'TOWNS/USDT', 'MBL/USDT', 'ALT/USDT', 'KAIA/USDT', 'JASMY/USDT', 'HEI/USDT', 'FXS/USDT', 'LUNC/USDT', 'GUN/USDT', 'STO/USDT', 'SFP/USDT', 'LAYER/USDT', 'CETUS/USDT', 'USTC/USDT', 'HIGH/USDT', 'JST/USDT', 'HOME/USDT', 'BABY/USDT', 'RESOLV/USDT', 'MAGIC/USDT', 'NOT/USDT', 'IOTX/USDT', 'RONIN/USDT', 'PUNDIX/USDT', 'KDA/USDT', 'DEXE/USDT', 'PYR/USDT', 'ASTR/USDT', 'COMP/USDT', 'API3/USDT', 'PARTI/USDT', 'ACH/USDT', 'TURBO/USDT', 'DOGS/USDT', 'XAI/USDT', 'ROSE/USDT', 'GLMR/USDT', 'DASH/USDT', 'PORTAL/USDT', 'EPIC/USDT', 'XTZ/USDT', 'CVX/USDT', 'IOTA/USDT', 'ZRX/USDT', 'NEWT/USDT', 'BMT/USDT', 'MANTA/USDT', 'COTI/USDT', 'HFT/USDT', 'METIS/USDT', 'ONE/USDT', 'LRC/USDT', 'NXPC/USDT', 'LUMIA/USDT', 'SOPH/USDT', 'TRU/USDT', 'BANANA/USDT', 'BLZ/USDT', 'LUNA/USDT', 'HNT/USDT', 'GMT/USDT', 'CYBER/USDT', 'SHELL/USDT', 'HAEDAL/USDT', 'AUCTION/USDT', '1INCH/USDT', 'NIL/USDT', 'ZIL/USDT', 'COOKIE/USDT', 'FLOW/USDT', 'ERA/USDT', 'MOVE/USDT', 'BAND/USDT', 'ILV/USDT', 'ANIME/USDT', 'SLP/USDT', 'CKB/USDT', 'VANRY/USDT', 'PERP/USDT', 'ACX/USDT', 'PHA/USDT', 'DYM/USDT', 'SUPER/USDT', 'TNSR/USDT', 'OMG/USDT', 'CELO/USDT', 'CGPT/USDT', 'SCR/USDT', 'ENJ/USDT', 'QI/USDT', 'GTC/USDT', 'NKN/USDT', 'ELF/USDT', 'XEC/USDT', 'ACE/USDT', 'CHR/USDT', 'QTUM/USDT', 'DGB/USDT', 'AVA/USDT', 'NFP/USDT', 'MASK/USDT', 'XMR/USDT', 'BSW/USDT', 'ANT/USDT', 'DODO/USDT', 'TLM/USDT', 'D/USDT', 'ANKR/USDT', 'HMSTR/USDT', 'OXT/USDT', 'VTHO/USDT', 'SXT/USDT', 'RPL/USDT', 'REN/USDT', 'NTRN/USDT', 'RDNT/USDT', 'KNC/USDT', 'ARPA/USDT', 'ETHUP/USDT', 'AGLD/USDT', 'GLM/USDT', 'ONT/USDT', 'OGN/USDT', 'WAVES/USDT', 'ICX/USDT', 'OSMO/USDT', 'UMA/USDT', 'ALPHA/USDT', 'DUSK/USDT', 'LTO/USDT', 'FORTH/USDT', 'MOVR/USDT', 'DENT/USDT', 'STORJ/USDT', 'REEF/USDT', 'SXP/USDT', 'AMP/USDT', 'AMB/USDT', 'AUDIO/USDT', 'DATA/USDT', 'DIA/USDT', 'SYN/USDT', 'CLV/USDT', 'TFUEL/USDT', 'BAT/USDT', 'IOST/USDT', 'T/USDT', 'FLUX/USDT', 'CELR/USDT', 'EPX/USDT', 'BIGTIME/USDT', 'BICO/USDT', 'XEM/USDT', 'QKC/USDT', 'POLS/USDT', 'CREAM/USDT', 'LSK/USDT', 'QUICK/USDT', 'DCR/USDT', 'GAS/USDT', 'POLYX/USDT', 'XNO/USDT', 'ADX/USDT', 'WAXP/USDT', 'UTK/USDT', 'STRAX/USDT', 'WIN/USDT', 'SYS/USDT', 'ATA/USDT', 'POND/USDT', 'BAL/USDT', 'KMD/USDT', 'CATI/USDT', 'WAN/USDT', 'G/USDT', 'ETHDOWN/USDT', 'VIDT/USDT', 'MTL/USDT', 'CVC/USDT', 'GNS/USDT', 'BTCDOWN/USDT', 'REQ/USDT', 'BTCUP/USDT', 'HARD/USDT', 'SCRT/USDT', 'AERGO/USDT', 'BSV/USDT', 'BTT/USDT', 'BULL/USDT', 'WLFI/USDT']
timeframes = ["15m", "30m", "1h", "2h", "4h", "1d", "1w"]

limit = 60
VOLUME_FACTOR = 3

# اطلاعات ایمیل از محیط امن GitHub Secrets خوانده می‌شود
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_TO = os.getenv("EMAIL_TO")

MAX_EMAIL_SIZE = 20 * 1024 * 1024  # 20MB

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
                    last_heavy_candle = candidate_candle
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
        print(f"Error in {symbol} {timeframe}: {e}")
        return None


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
        print(f"Error plotting {symbol} {timeframe}: {e}")
        return None


def send_email(subject, body, images):
    if not EMAIL_USER or not EMAIL_PASS or not EMAIL_TO:
        print("❌ Environment variables for email not set.")
        return

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
            print(f"Error attaching {img_path}: {e}")

    try:
        server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT)
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()
        print(f"📧 Email sent: {subject}")
    except Exception as e:
        print("❌ Error sending email:", e)


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
            if chart_file:
                size = os.path.getsize(chart_file)
                charts_info.append((sym, tf, chart_file, size))

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
        body = ""
        images = []
        for sym, tf, path in batch:
            ticker = exchange.fetch_ticker(sym)
            quote_volume = ticker.get('quoteVolume') or 0
            last_price = ticker.get('last') or 0
            volume_usd_24h = quote_volume * last_price
            body += f"{sym}: {tf} (24h Volume USD: {volume_usd_24h:.2f})\n"
            images.append(path)
        send_email(f"Trade Positions Report - Part {idx}", body, images)


if __name__ == "__main__":
    main()
