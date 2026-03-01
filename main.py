"""
danal — 핀테크 & 디지털자산 투자 리서치 자동화

사용법:
  python main.py --brief                  # 주간 핀테크 브리핑
  python main.py --im "Circle"            # 투자 검토 보고서 초안
  python main.py --screen stablecoin      # 시장 스크리닝
"""

import argparse
from src.collect import collect
from src.research import research
from src.report import report


def run_brief():
    print("── 주간 브리핑 생성 중 ──")
    collect(mode="brief")
    path = report(report_type="brief")
    print(f"\n✓ 완료: {path}")


def run_im(company: str):
    print(f"── IM 초안 생성 중: {company} ──")
    research(company=company)
    path = report(report_type="im", company=company)
    print(f"\n✓ 완료: {path}")


def run_screen(sector: str):
    print(f"── 시장 스크리닝 중: {sector} ──")
    collect(mode="screen", sector=sector)
    path = report(report_type="screen")
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
    args = parser.parse_args()

    if args.brief:
        run_brief()
    elif args.im:
        run_im(args.im)
    elif args.screen:
        run_screen(args.screen)
