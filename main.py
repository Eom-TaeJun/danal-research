"""
danal — 핀테크 & 디지털자산 투자 리서치 자동화

사용법:
  python main.py --brief                  # 주간 핀테크 브리핑
  python main.py --im "Circle"            # 투자 검토 보고서 초안
  python main.py --screen stablecoin      # 시장 스크리닝
  python main.py --deep stablecoin        # 스테이블코인 심화 분석
  python main.py --calibrate             # 신호 가중치 자동 보정
"""

import argparse
from src.collect import collect
from src.research import research
from src.report import report
from src.analyze import analyze


def run_brief():
    print("── 주간 브리핑 생성 중 ──")
    collect(mode="brief")
    analyze()
    path = report(report_type="brief")
    print(f"\n✓ 완료: {path}")


def run_im(company: str):
    print(f"── IM 초안 생성 중: {company} ──")
    research(company=company)
    path = report(report_type="im", company=company)
    print(f"\n✓ 완료: {path}")


def run_analyze():
    print("── 레짐 분석 중 ──")
    result = analyze()
    r = result.get("regime", {})
    s = result.get("stablecoin_signal", {})
    print(f"  레짐: {r.get('regime')} (확신: {r.get('confidence')})")
    for line in r.get("rationale", []):
        print(f"  • {line}")
    print(f"  스테이블코인: {s.get('note')}")
    print(f"\n✓ 완료: outputs/context/analysis_*.json")


def run_screen(sector: str):
    print(f"── 시장 스크리닝 중: {sector} ──")
    collect(mode="screen", sector=sector)
    analyze()
    path = report(report_type="screen")
    print(f"\n✓ 완료: {path}")


def run_deep(topic: str):
    print(f"── 심화 리포트 생성 중: {topic} ──")
    collect(mode="deep")
    analyze()
    path = report(report_type="deep")
    print(f"\n✓ 완료: {path}")


def run_calibrate():
    print("── 신호 가중치 보정 중 ──")
    from src.calibrate import calibrate
    result = calibrate()
    meta = result.get("meta", {})
    print(f"  방법: {meta.get('method')} (samples={meta.get('samples', 0)})")
    if result.get("correlations"):
        print("  신호별 상관:")
        for name, rho in sorted(result["correlations"].items(),
                                 key=lambda x: abs(x[1]), reverse=True):
            print(f"    {name}: {rho:+.3f}")
    print(f"\n✓ 완료: outputs/context/weights_*.json")


def run_excel():
    print("── Excel 변환 중 ──")
    from src.excel import generate_excel

    path = generate_excel()
    print(f"\n✓ 완료: {path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="danal — 핀테크 & 디지털자산 투자 리서치 자동화"
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--brief", action="store_true",
                       help="주간 핀테크/디지털자산 브리핑 생성")
    group.add_argument("--im", metavar="COMPANY",
                       help="투자 검토 보고서(IM) 초안 작성")
    group.add_argument("--screen", metavar="SECTOR",
                       help="섹터 스크리닝 (stablecoin / fintech / defi)")
    group.add_argument("--analyze", action="store_true",
                       help="거시 레짐 판단 + 스테이블코인 시그널 분석")
    group.add_argument("--deep", metavar="TOPIC",
                       help="심화 리포트 (stablecoin)")
    group.add_argument("--calibrate", action="store_true",
                       help="과거 분석 결과 기반 신호 가중치 자동 보정")
    group.add_argument("--excel", action="store_true",
                       help="CSV 데이터를 Excel(.xlsx)로 변환 출력")
    args = parser.parse_args()

    if args.brief:
        run_brief()
    elif args.im:
        run_im(args.im)
    elif args.screen:
        run_screen(args.screen)
    elif args.analyze:
        run_analyze()
    elif args.deep:
        run_deep(args.deep)
    elif args.calibrate:
        run_calibrate()
    elif args.excel:
        run_excel()
