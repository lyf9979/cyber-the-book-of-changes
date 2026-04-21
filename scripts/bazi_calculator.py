#!/usr/bin/env python3
"""
赛博周易 · 四柱八字排盘工具
Cyber Book of Changes - Bazi Calculator

使用权威开源历法库 sxtwl（寿星天文历）保证排盘精度。

使用示例：
    python bazi_calculator.py --date 1988-06-15 --time 09:30 --gender female
    python bazi_calculator.py --date 1990-05-15 --time 14:30 --gender female --longitude 114
    python bazi_calculator.py --date 1988-06-15 --time 09:30 --gender female --json

依赖安装：
    pip install sxtwl

注：此脚本仅提供权威排盘数据。完整命理分析由 LLM 结合 references/ 中的知识库完成。
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict, field
from typing import List, Tuple, Dict, Optional

try:
    import sxtwl
except ImportError:
    print("错误：缺少依赖库 sxtwl", file=sys.stderr)
    print("请运行：pip install sxtwl", file=sys.stderr)
    sys.exit(1)


# ========== 基础数据 ==========

TIANGAN = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
DIZHI = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']

WUXING = {
    '甲': '木', '乙': '木', '丙': '火', '丁': '火', '戊': '土',
    '己': '土', '庚': '金', '辛': '金', '壬': '水', '癸': '水',
    '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土',
    '巳': '火', '午': '火', '未': '土', '申': '金', '酉': '金',
    '戌': '土', '亥': '水'
}

YINYANG = {
    '甲': '阳', '乙': '阴', '丙': '阳', '丁': '阴', '戊': '阳',
    '己': '阴', '庚': '阳', '辛': '阴', '壬': '阳', '癸': '阴',
    '子': '阳', '丑': '阴', '寅': '阳', '卯': '阴', '辰': '阳',
    '巳': '阴', '午': '阳', '未': '阴', '申': '阳', '酉': '阴',
    '戌': '阳', '亥': '阴'
}

ZANGGAN: Dict[str, List[str]] = {
    '子': ['癸'],
    '丑': ['己', '癸', '辛'],
    '寅': ['甲', '丙', '戊'],
    '卯': ['乙'],
    '辰': ['戊', '乙', '癸'],
    '巳': ['丙', '庚', '戊'],
    '午': ['丁', '己'],
    '未': ['己', '丁', '乙'],
    '申': ['庚', '壬', '戊'],
    '酉': ['辛'],
    '戌': ['戊', '辛', '丁'],
    '亥': ['壬', '甲']
}


def get_shishen(ri_gan: str, other_gan: str) -> str:
    """计算十神关系（以日干为中心）"""
    if ri_gan == other_gan:
        return '比肩'

    ri_wx = WUXING[ri_gan]
    other_wx = WUXING[other_gan]
    same_yy = (YINYANG[ri_gan] == YINYANG[other_gan])

    if ri_wx == other_wx:
        return '比肩' if same_yy else '劫财'

    sheng = {'木': '火', '火': '土', '土': '金', '金': '水', '水': '木'}
    ke = {'木': '土', '火': '金', '土': '水', '金': '木', '水': '火'}

    if sheng[ri_wx] == other_wx:
        return '食神' if same_yy else '伤官'
    elif ke[ri_wx] == other_wx:
        return '偏财' if same_yy else '正财'
    elif ke[other_wx] == ri_wx:
        return '七杀' if same_yy else '正官'
    else:
        return '偏印' if same_yy else '正印'


# ========== 神煞 ==========

TIANYI_GUIREN = {
    '甲': ['丑', '未'], '戊': ['丑', '未'], '庚': ['丑', '未'],
    '乙': ['子', '申'], '己': ['子', '申'],
    '丙': ['亥', '酉'], '丁': ['亥', '酉'],
    '壬': ['卯', '巳'], '癸': ['卯', '巳'],
    '辛': ['寅', '午']
}
TAOHUA = {'申':'酉','子':'酉','辰':'酉','寅':'卯','午':'卯','戌':'卯',
          '巳':'午','酉':'午','丑':'午','亥':'子','卯':'子','未':'子'}
YIMA = {'申':'寅','子':'寅','辰':'寅','寅':'申','午':'申','戌':'申',
        '巳':'亥','酉':'亥','丑':'亥','亥':'巳','卯':'巳','未':'巳'}
HUAGAI = {'申':'辰','子':'辰','辰':'辰','寅':'戌','午':'戌','戌':'戌',
          '巳':'丑','酉':'丑','丑':'丑','亥':'未','卯':'未','未':'未'}
YANGREN = {'甲':'卯','乙':'辰','丙':'午','丁':'未','戊':'午',
           '己':'未','庚':'酉','辛':'戌','壬':'子','癸':'丑'}
WENCHANG = {'甲':'巳','乙':'午','丙':'申','戊':'申','丁':'酉',
            '己':'酉','庚':'亥','辛':'子','壬':'寅','癸':'卯'}


def calculate_shensha(year_zhi: str, day_zhi: str, day_gan: str,
                     all_zhis: List[str]) -> Dict[str, List[str]]:
    result = {}
    tianyi = TIANYI_GUIREN.get(day_gan, [])
    hits = [z for z in all_zhis if z in tianyi]
    if hits:
        result['天乙贵人'] = hits

    taohua_y = TAOHUA.get(year_zhi)
    taohua_d = TAOHUA.get(day_zhi)
    th = [z for z in all_zhis if z == taohua_y or z == taohua_d]
    if th:
        result['桃花'] = th

    yima_y = YIMA.get(year_zhi)
    yima_d = YIMA.get(day_zhi)
    ym = [z for z in all_zhis if z == yima_y or z == yima_d]
    if ym:
        result['驿马'] = ym

    hg_y = HUAGAI.get(year_zhi)
    hg_d = HUAGAI.get(day_zhi)
    hg = [z for z in all_zhis if z == hg_y or z == hg_d]
    if hg:
        result['华盖'] = hg

    yr = YANGREN.get(day_gan)
    if yr in all_zhis:
        result['羊刃'] = [yr]

    wc = WENCHANG.get(day_gan)
    if wc in all_zhis:
        result['文昌'] = [wc]

    return result


# ========== 大运计算 ==========

def calculate_dayun(y_gan: str, m_gan: str, m_zhi: str,
                    gender: str, birth_date: datetime,
                    num_steps: int = 8) -> Tuple[float, List[Dict]]:
    """使用 sxtwl 精确节气计算起运与大运"""
    is_yang_year = YINYANG[y_gan] == '阳'
    forward = (is_yang_year and gender == 'male') or \
              (not is_yang_year and gender == 'female')

    # 收集出生年前后的"节"（12 个节，不含"气"）
    # 节气索引：0立春 3惊蛰 6清明 9立夏 12芒种 15小暑 18立秋 21白露 23寒露
    # 实际 sxtwl 索引映射：见官方文档
    # 用 getJieQiByYear 取所有节气，按时间排序
    jieqi_list = []
    for y in [birth_date.year - 1, birth_date.year, birth_date.year + 1]:
        try:
            jq_infos = sxtwl.getJieQiByYear(y)
            for info in jq_infos:
                jd = info.jd
                t = sxtwl.JD2DD(jd)
                jq_dt = datetime(int(t.Y), int(t.M), int(t.D),
                                int(t.h), int(t.m), max(0, int(t.s)))
                # jqIndex: 立春=2, 惊蛰=4, 清明=6, 立夏=8, 芒种=10,
                # 小暑=12, 立秋=14, 白露=16, 寒露=18, 立冬=20, 大雪=22, 小寒=0
                if info.jqIndex in [0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22]:
                    jieqi_list.append(jq_dt)
        except Exception as e:
            pass

    jieqi_list.sort()

    # 找前后节
    prev_jq = None
    next_jq = None
    for jq in jieqi_list:
        if jq <= birth_date:
            prev_jq = jq
        else:
            next_jq = jq
            break

    if forward:
        delta = (next_jq - birth_date).total_seconds() if next_jq else 0
    else:
        delta = (birth_date - prev_jq).total_seconds() if prev_jq else 0

    days = delta / 86400
    start_age = days / 3.0  # 3 天 = 1 岁

    # 六十甲子序列
    jiazi = []
    for i in range(60):
        jiazi.append((TIANGAN[i % 10], DIZHI[i % 12]))

    try:
        month_idx = jiazi.index((m_gan, m_zhi))
    except ValueError:
        month_idx = 0

    dayun = []
    for i in range(1, num_steps + 1):
        step_idx = (month_idx + i) % 60 if forward else (month_idx - i) % 60
        g, z = jiazi[step_idx]
        start = start_age + (i - 1) * 10
        end = start + 10
        dayun.append({
            'pillar': f'{g}{z}',
            'gan': g,
            'zhi': z,
            'start_age': round(start, 1),
            'end_age': round(end, 1),
            'start_year': birth_date.year + int(start),
            'end_year': birth_date.year + int(end),
        })

    return start_age, dayun


def adjust_true_solar_time(dt: datetime, longitude: float = 120.0) -> datetime:
    if abs(longitude - 120.0) < 0.01:
        return dt
    delta_minutes = (longitude - 120.0) * 4
    return dt + timedelta(minutes=delta_minutes)


# ========== 主排盘 ==========

@dataclass
class BaziResult:
    input: Dict
    pillars: Dict
    zanggan: Dict
    shishen: Dict
    wuxing_count: Dict
    shensha: Dict
    ri_zhu: Dict
    dayun: List[Dict]
    current_dayun: Optional[Dict] = None
    next_three_years: List[Dict] = field(default_factory=list)


def calculate_bazi(date_str: str, time_str: str, gender: str,
                   longitude: float = 120.0,
                   use_late_zishi: bool = False) -> BaziResult:
    year, month, day = map(int, date_str.split('-'))
    hour, minute = map(int, time_str.split(':'))

    birth_raw = datetime(year, month, day, hour, minute)
    birth_dt = adjust_true_solar_time(birth_raw, longitude)

    y, m, d = birth_dt.year, birth_dt.month, birth_dt.day
    h = birth_dt.hour

    sxtwl_day = sxtwl.fromSolar(y, m, d)
    yGZ = sxtwl_day.getYearGZ()
    mGZ = sxtwl_day.getMonthGZ()
    dGZ = sxtwl_day.getDayGZ()

    y_gan, y_zhi = TIANGAN[yGZ.tg], DIZHI[yGZ.dz]
    m_gan, m_zhi = TIANGAN[mGZ.tg], DIZHI[mGZ.dz]
    d_gan, d_zhi = TIANGAN[dGZ.tg], DIZHI[dGZ.dz]

    hGZ = sxtwl.getShiGz(dGZ.tg, h, use_late_zishi)
    h_gan, h_zhi = TIANGAN[hGZ.tg], DIZHI[hGZ.dz]

    zanggan = {
        'year': ZANGGAN[y_zhi],
        'month': ZANGGAN[m_zhi],
        'day': ZANGGAN[d_zhi],
        'hour': ZANGGAN[h_zhi],
    }

    shishen = {
        'year_gan': get_shishen(d_gan, y_gan),
        'month_gan': get_shishen(d_gan, m_gan),
        'hour_gan': get_shishen(d_gan, h_gan),
        'year_zhi_hidden': [[zg, get_shishen(d_gan, zg)] for zg in ZANGGAN[y_zhi]],
        'month_zhi_hidden': [[zg, get_shishen(d_gan, zg)] for zg in ZANGGAN[m_zhi]],
        'day_zhi_hidden': [[zg, get_shishen(d_gan, zg)] for zg in ZANGGAN[d_zhi]],
        'hour_zhi_hidden': [[zg, get_shishen(d_gan, zg)] for zg in ZANGGAN[h_zhi]],
    }

    # 五行加权
    wx_count = {'金': 0.0, '木': 0.0, '水': 0.0, '火': 0.0, '土': 0.0}
    for g in [y_gan, m_gan, d_gan, h_gan]:
        wx_count[WUXING[g]] += 1
    for zhi in [y_zhi, m_zhi, d_zhi, h_zhi]:
        hidden = ZANGGAN[zhi]
        weights = [1.0, 0.5, 0.3][:len(hidden)]
        for zg, w in zip(hidden, weights):
            wx_count[WUXING[zg]] += w
    wx_count = {k: round(v, 1) for k, v in wx_count.items()}

    all_zhis = [y_zhi, m_zhi, d_zhi, h_zhi]
    shensha = calculate_shensha(y_zhi, d_zhi, d_gan, all_zhis)

    start_age, dayun = calculate_dayun(y_gan, m_gan, m_zhi, gender, birth_dt)

    now = datetime.now()
    current_age = (now - birth_dt).days / 365.25
    current_dayun = None
    for du in dayun:
        if du['start_age'] <= current_age < du['end_age']:
            current_dayun = du
            break

    # 近三年流年
    jiazi = [(TIANGAN[i % 10], DIZHI[i % 12]) for i in range(60)]
    next_three_years = []
    for i in range(3):
        ly_year = now.year + i
        ly_idx = (ly_year - 1984) % 60
        ly_gan, ly_zhi = jiazi[ly_idx]
        next_three_years.append({
            'year': ly_year,
            'pillar': f'{ly_gan}{ly_zhi}',
            'gan': ly_gan,
            'zhi': ly_zhi,
            'gan_shishen': get_shishen(d_gan, ly_gan),
            'zhi_wuxing': WUXING[ly_zhi],
        })

    return BaziResult(
        input={
            'date': date_str,
            'time': time_str,
            'adjusted_datetime': birth_dt.strftime('%Y-%m-%d %H:%M'),
            'gender': gender,
            'longitude': longitude,
            'use_late_zishi': use_late_zishi,
        },
        pillars={
            'year': {'gan': y_gan, 'zhi': y_zhi, 'pillar': f'{y_gan}{y_zhi}'},
            'month': {'gan': m_gan, 'zhi': m_zhi, 'pillar': f'{m_gan}{m_zhi}'},
            'day': {'gan': d_gan, 'zhi': d_zhi, 'pillar': f'{d_gan}{d_zhi}'},
            'hour': {'gan': h_gan, 'zhi': h_zhi, 'pillar': f'{h_gan}{h_zhi}'},
        },
        zanggan=zanggan,
        shishen=shishen,
        wuxing_count=wx_count,
        shensha=shensha,
        ri_zhu={
            'gan': d_gan,
            'wuxing': WUXING[d_gan],
            'yinyang': YINYANG[d_gan],
            'description': f'{YINYANG[d_gan]}{WUXING[d_gan]}',
        },
        dayun=dayun,
        current_dayun=current_dayun,
        next_three_years=next_three_years,
    )


# ========== 输出 ==========

def format_result(result: BaziResult) -> str:
    out = []
    out.append("=" * 66)
    out.append("                   赛博周易 · 四柱八字排盘")
    out.append("                Cyber Book of Changes")
    out.append("=" * 66)
    out.append("")

    out.append("【基本信息】")
    out.append(f"  公历生日：{result.input['date']} {result.input['time']}")
    if result.input['longitude'] != 120.0:
        out.append(f"  经度：东经 {result.input['longitude']}°（真太阳时校正）")
        out.append(f"  校正后：{result.input['adjusted_datetime']}")
    out.append(f"  性别：{'男' if result.input['gender'] == 'male' else '女'}")
    zishi_mode = '古法（晚子时归当日）' if result.input['use_late_zishi'] else '现代（00点后归次日）'
    out.append(f"  子时算法：{zishi_mode}")
    out.append("")

    p = result.pillars
    out.append("【四柱八字】")
    out.append("  ┌────────┬────────┬────────┬────────┐")
    out.append("  │  年柱  │  月柱  │  日柱  │  时柱  │")
    out.append("  ├────────┼────────┼────────┼────────┤")
    out.append(f"  │   {p['year']['gan']}    │   {p['month']['gan']}    │  {p['day']['gan']}★   │   {p['hour']['gan']}    │")
    out.append(f"  │   {p['year']['zhi']}    │   {p['month']['zhi']}    │   {p['day']['zhi']}    │   {p['hour']['zhi']}    │")
    out.append("  └────────┴────────┴────────┴────────┘")
    out.append(f"        ★ 日主：{result.ri_zhu['gan']}（{result.ri_zhu['description']}）")
    out.append("")

    out.append("【十神排布】（以日干为中心）")
    out.append(f"  年干 {p['year']['gan']} → {result.shishen['year_gan']}")
    out.append(f"  月干 {p['month']['gan']} → {result.shishen['month_gan']}")
    out.append(f"  时干 {p['hour']['gan']} → {result.shishen['hour_gan']}")
    out.append("")

    out.append("【地支藏干 · 十神】")
    for pos, name in [('year', '年支'), ('month', '月支'),
                      ('day', '日支'), ('hour', '时支')]:
        zhi = p[pos]['zhi']
        hidden = result.shishen[f'{pos}_zhi_hidden']
        items = [f'{g}({s})' for g, s in hidden]
        out.append(f"  {name} {zhi}：{' / '.join(items)}")
    out.append("")

    out.append("【五行力量】（含藏干加权）")
    wx = result.wuxing_count
    max_wx = max(wx.values()) if max(wx.values()) > 0 else 1
    for name, val in wx.items():
        bar_len = int(val / max_wx * 20)
        bar = '█' * bar_len
        out.append(f"  {name}：{val:>5}  {bar}")
    out.append("")

    if result.shensha:
        out.append("【神煞】")
        for name, positions in result.shensha.items():
            out.append(f"  {name}：{' '.join(positions)}")
        out.append("")

    out.append("【大运排列】")
    ri_gan = result.ri_zhu['gan']
    for i, du in enumerate(result.dayun):
        marker = "  ← 当前大运" if result.current_dayun and du['pillar'] == result.current_dayun['pillar'] else ""
        ss_gan = get_shishen(ri_gan, du['gan'])
        out.append(
            f"  第{i+1}步：{du['pillar']}  "
            f"{du['start_age']:>5.1f} - {du['end_age']:>5.1f}岁  "
            f"({du['start_year']}-{du['end_year']})  "
            f"{ss_gan}{marker}"
        )
    out.append("")

    out.append("【近三年流年】")
    for ly in result.next_three_years:
        out.append(
            f"  {ly['year']} 年 {ly['pillar']}  "
            f"天干十神：{ly['gan_shishen']}  "
            f"地支五行：{ly['zhi_wuxing']}"
        )
    out.append("")

    out.append("=" * 66)
    out.append("  ⚠️  基于寿星天文历 sxtwl 库的权威排盘数据")
    out.append("      完整命理解读请交由具备本 skill 能力的 LLM 完成")
    out.append("      传统命理仅供文化参考，不构成人生决策依据")
    out.append("=" * 66)

    return "\n".join(out)


def format_json(result: BaziResult) -> str:
    return json.dumps(asdict(result), ensure_ascii=False, indent=2)


def main():
    parser = argparse.ArgumentParser(
        description="赛博周易 · 四柱八字权威排盘工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例：
  python bazi_calculator.py --date 1988-06-15 --time 09:30 --gender female
  python bazi_calculator.py --date 1990-05-15 --time 14:30 --gender female --longitude 114.3
  python bazi_calculator.py --date 1988-06-15 --time 09:30 --gender female --json
        """
    )
    parser.add_argument('--date', required=True, help='出生日期 YYYY-MM-DD（公历）')
    parser.add_argument('--time', required=True, help='出生时间 HH:MM（24 小时制）')
    parser.add_argument('--gender', required=True, choices=['male', 'female'])
    parser.add_argument('--longitude', type=float, default=120.0,
                       help='出生地经度（默认 120，北京标准时）')
    parser.add_argument('--late-zishi', action='store_true',
                       help='使用古法子时（晚子时归当日）')
    parser.add_argument('--json', action='store_true',
                       help='JSON 格式输出（便于 LLM 消费）')

    args = parser.parse_args()

    try:
        result = calculate_bazi(
            args.date, args.time, args.gender,
            args.longitude, args.late_zishi
        )
        if args.json:
            print(format_json(result))
        else:
            print(format_result(result))
    except Exception as e:
        print(f"排盘出错：{e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
