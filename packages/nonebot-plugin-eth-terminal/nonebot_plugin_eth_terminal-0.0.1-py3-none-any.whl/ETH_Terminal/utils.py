import httpx
import time


def get_mid(t: str, a: str, b: str) -> str:
    i = t.find(a, 0, len(t))
    e = t.find(b, i, len(t))
    mid = t[i+len(a):e]
    return mid


def format(time_str: str) -> str:
    d = time_str.split()
    d.remove("Sep")
    d.remove("UTC")
    t = d[2].split(":")
    if len(t) != 3:
        t.append("00")

    st = time.localtime(
        time.mktime(
            time.strptime(
                f"{d[1]} Sep {t[0]} {t[1]} {t[2]} {d[3]} UTC",
                r"%d %b %H %M %S %Y %Z"
            )
        ) + (8 * 60 * 60)
    )
    return f"{st.tm_year}年{st.tm_mon}月{st.tm_mday}日 {st.tm_hour}:{st.tm_min}:{st.tm_sec}"


async def check_terminal():
    async with httpx.AsyncClient() as client:
        re_value = await client.get('https://bordel.wtf/')
        text = re_value.text

    TTD_time = format(get_mid(text, "is expected around ", ", i.e."))
    finish_time = format(get_mid(text, "last update at:\n", "\n<p></p>"))
    hashrate = get_mid(text, "<p>Current daily hashrate: ", "</p>")

    return f"预计合并时间: {TTD_time}\n" \
        f"当前哈希值: {hashrate}\n" \
        f"更新时间: {finish_time}"
