#!/usr/bin/env python3
"""
신고내역 삭제 스크립트
사용법: python delete_reports.py [옵션]
"""

import sqlite3
import sys
import argparse

def delete_all_reports():
    """모든 신고 삭제"""
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    
    # 삭제 전 개수 확인
    cursor.execute('SELECT COUNT(*) FROM reports')
    count = cursor.fetchone()[0]
    
    if count == 0:
        print("삭제할 신고가 없습니다.")
        conn.close()
        return
    
    # 확인 메시지
    confirm = input(f"정말로 {count}개의 신고를 모두 삭제하시겠습니까? (y/N): ")
    if confirm.lower() != 'y':
        print("삭제가 취소되었습니다.")
        conn.close()
        return
    
    # 삭제 실행
    cursor.execute('DELETE FROM reports')
    conn.commit()
    conn.close()
    
    print(f"✅ 총 {count}개의 신고가 삭제되었습니다.")

def delete_report_by_id(report_id):
    """특정 신고 삭제"""
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    
    # 신고 존재 확인
    cursor.execute('SELECT id, damage_type, status FROM reports WHERE id = ?', (report_id,))
    report = cursor.fetchone()
    
    if not report:
        print(f"❌ 신고 #{report_id}를 찾을 수 없습니다.")
        conn.close()
        return
    
    # 확인 메시지
    print(f"신고 #{report_id} 정보:")
    print(f"  - 손상유형: {report[1]}")
    print(f"  - 상태: {report[2]}")
    
    confirm = input("이 신고를 삭제하시겠습니까? (y/N): ")
    if confirm.lower() != 'y':
        print("삭제가 취소되었습니다.")
        conn.close()
        return
    
    # 삭제 실행
    cursor.execute('DELETE FROM reports WHERE id = ?', (report_id,))
    conn.commit()
    conn.close()
    
    print(f"✅ 신고 #{report_id}가 삭제되었습니다.")

def delete_reports_by_status(status):
    """상태별 신고 삭제"""
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    
    # 해당 상태의 신고 개수 확인
    cursor.execute('SELECT COUNT(*) FROM reports WHERE status = ?', (status,))
    count = cursor.fetchone()[0]
    
    if count == 0:
        print(f"'{status}' 상태의 신고가 없습니다.")
        conn.close()
        return
    
    # 확인 메시지
    confirm = input(f"'{status}' 상태의 {count}개 신고를 삭제하시겠습니까? (y/N): ")
    if confirm.lower() != 'y':
        print("삭제가 취소되었습니다.")
        conn.close()
        return
    
    # 삭제 실행
    cursor.execute('DELETE FROM reports WHERE status = ?', (status,))
    conn.commit()
    conn.close()
    
    print(f"✅ '{status}' 상태의 {count}개 신고가 삭제되었습니다.")

def show_reports():
    """현재 신고 목록 표시"""
    conn = sqlite3.connect('reports.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT id, damage_type, status, urgency_level, created_at 
        FROM reports 
        ORDER BY created_at DESC
    ''')
    
    reports = cursor.fetchall()
    conn.close()
    
    if not reports:
        print("현재 신고가 없습니다.")
        return
    
    print(f"\n📋 현재 신고 목록 ({len(reports)}개):")
    print("-" * 80)
    print(f"{'ID':<5} {'손상유형':<10} {'상태':<8} {'긴급도':<6} {'접수일':<20}")
    print("-" * 80)
    
    for report in reports:
        urgency_text = ['낮음', '보통', '높음', '매우높음', '긴급'][report[3] - 1]
        print(f"{report[0]:<5} {report[1]:<10} {report[2]:<8} {urgency_text:<6} {report[4]:<20}")

def main():
    parser = argparse.ArgumentParser(description='신고내역 삭제 도구')
    parser.add_argument('--all', action='store_true', help='모든 신고 삭제')
    parser.add_argument('--id', type=int, help='특정 신고 ID 삭제')
    parser.add_argument('--status', type=str, help='특정 상태의 신고 삭제 (접수, 검토중, 처리중, 완료)')
    parser.add_argument('--list', action='store_true', help='현재 신고 목록 표시')
    
    args = parser.parse_args()
    
    if args.list:
        show_reports()
    elif args.all:
        delete_all_reports()
    elif args.id:
        delete_report_by_id(args.id)
    elif args.status:
        valid_statuses = ['접수', '검토중', '처리중', '완료']
        if args.status not in valid_statuses:
            print(f"❌ 유효하지 않은 상태입니다. 가능한 상태: {', '.join(valid_statuses)}")
            return
        delete_reports_by_status(args.status)
    else:
        print("사용법:")
        print("  python delete_reports.py --list          # 신고 목록 보기")
        print("  python delete_reports.py --all           # 모든 신고 삭제")
        print("  python delete_reports.py --id 1          # 특정 신고 삭제")
        print("  python delete_reports.py --status 완료    # 완료된 신고만 삭제")

if __name__ == "__main__":
    main()
