"""
扩展演示数据脚本
Extended Demo Data Script
"""
from datetime import datetime, timedelta
from database import SessionLocal
from models import (
    User, Organization, Award, AwardCycle, Application,
    Review, CommitteeDecision, Announcement,
    UserRole, OrgType, AwardLevel, ApplicationStatus
)
from crud.user import get_password_hash


def add_extended_data():
    """添加扩展演示数据"""
    db = SessionLocal()
    
    try:
        print("\n开始添加扩展演示数据...")
        
        # 检查是否已添加
        existing_orgs = db.query(Organization).filter(Organization.code == "ORG006").count()
        if existing_orgs > 0:
            print("\n检测到扩展数据已存在,跳过添加")
            print_statistics(db)
            return
        
        # 1. 添加更多组织
        print("\n1. 添加组织...")
        new_orgs = [
            Organization(
                name="XX冶金科技有限公司",
                code="ORG006",
                org_type=OrgType.ENTERPRISE,
                contact_person="周总",
                contact_phone="0411-88888888",
                email="contact@metallurgy.com",
                address="辽宁省大连市"
            ),
            Organization(
                name="XX稀土研究所",
                code="ORG007",
                org_type=OrgType.INSTITUTE,
                contact_person="吴所长",
                contact_phone="0471-88888888",
                email="contact@rareearth.com",
                address="内蒙古包头市"
            ),
            Organization(
                name="XX工业大学材料学院",
                code="ORG008",
                org_type=OrgType.UNIVERSITY,
                contact_person="郑教授",
                contact_phone="024-88888888",
                email="contact@material.edu",
                address="辽宁省沈阳市"
            )
        ]
        
        for org in new_orgs:
            db.add(org)
        db.commit()
        print(f"✓ 添加了 {len(new_orgs)} 个组织")
        
        # 2. 添加更多用户
        print("\n2. 添加用户...")
        new_users = [
            User(
                username="expert04",
                password_hash=get_password_hash("expert123"),
                real_name="孙教授",
                email="expert04@university.edu",
                mobile="13800138010",
                role=UserRole.EXPERT,
                organization_id=8
            ),
            User(
                username="expert05",
                password_hash=get_password_hash("expert123"),
                real_name="周高工",
                email="expert05@metallurgy.com",
                mobile="13800138011",
                role=UserRole.EXPERT,
                organization_id=6
            ),
            User(
                username="applicant03",
                password_hash=get_password_hash("app123"),
                real_name="钱工程师",
                email="applicant03@aluminum.com",
                mobile="13800138012",
                role=UserRole.APPLICANT,
                organization_id=5
            ),
            User(
                username="applicant04",
                password_hash=get_password_hash("app123"),
                real_name="孙研究员",
                email="applicant04@rareearth.com",
                mobile="13800138013",
                role=UserRole.APPLICANT,
                organization_id=7
            ),
            User(
                username="committee02",
                password_hash=get_password_hash("comm123"),
                real_name="马委员",
                email="committee02@nonferrous.org",
                mobile="13800138014",
                role=UserRole.COMMITTEE,
                organization_id=1
            )
        ]
        
        for user in new_users:
            db.add(user)
        db.commit()
        print(f"✓ 添加了 {len(new_users)} 个用户")
        
        # 3. 添加更多奖项
        print("\n3. 添加奖项...")
        new_awards = [
            Award(
                name="XXXX协会科学技术奖 - 青年科技创新奖",
                code="AWARD2024-03",
                level=AwardLevel.INDUSTRY,
                year=2024,
                description="表彰在科技领域做出突出贡献的青年科技工作者",
                application_start=datetime.now() - timedelta(days=20),
                application_end=datetime.now() + timedelta(days=70),
                status="active",
                created_by=1
            ),
            Award(
                name="XXXX协会科学技术奖 - 企业技术创新奖",
                code="AWARD2024-04",
                level=AwardLevel.INDUSTRY,
                year=2024,
                description="表彰在企业技术创新方面表现突出的项目",
                application_start=datetime.now() - timedelta(days=25),
                application_end=datetime.now() + timedelta(days=65),
                status="active",
                created_by=1
            )
        ]
        
        for award in new_awards:
            db.add(award)
        db.commit()
        print(f"✓ 添加了 {len(new_awards)} 个奖项")
        
        # 4. 添加更多申报
        print("\n4. 添加申报...")
        new_applications = [
            Application(
                award_cycle_id=1,
                applicant_unit_id=5,
                applicant_user_id=11,
                title="新型高强铝合金材料研发及应用",
                category="技术发明",
                leader_name="钱工程师",
                leader_title="高级工程师",
                team_members="孙工,李工,赵工,王工",
                summary="针对航空航天领域需求,开发新型高强铝合金材料",
                technical_details="采用创新性合金设计理念,优化热处理工艺,显著提高材料强度和韧性",
                innovation_points="1.创新合金成分设计; 2.优化热处理工艺; 3.提高材料综合性能30%",
                application_value="可应用于航空航天、交通运输等高端领域",
                economic_benefit="近三年实现销售额8000万元,利润1500万元",
                social_benefit="替代进口材料,降低成本40%,推动产业升级",
                submission_status=ApplicationStatus.EXPERT_REVIEW,
                submission_time=datetime.now() - timedelta(days=18),
                current_stage="专家评审中"
            ),
            Application(
                award_cycle_id=1,
                applicant_unit_id=7,
                applicant_user_id=12,
                title="稀土功能材料制备关键技术研究",
                category="科技进步",
                leader_name="孙研究员",
                leader_title="研究员",
                team_members="吴工,郑工,冯工",
                summary="开发稀土功能材料制备关键技术,实现产业化应用",
                technical_details="突破材料纯化、成型、烧结等关键工艺",
                innovation_points="1.开发高纯化技术; 2.优化成型工艺; 3.提高产品性能50%",
                application_value="广泛应用于电子、光学、催化等领域",
                economic_benefit="年产值5000万元,利润1200万元",
                social_benefit="降低稀土资源消耗20%,减少环境污染",
                submission_status=ApplicationStatus.REVIEWING,
                submission_time=datetime.now() - timedelta(days=25),
                current_stage="终审中"
            ),
            Application(
                award_cycle_id=1,
                applicant_unit_id=6,
                applicant_user_id=6,
                title="铜基复合材料制备新技术",
                category="技术发明",
                leader_name="张工程师",
                leader_title="高级工程师",
                team_members="李工,王工",
                summary="开发铜基复合材料制备新技术,提高材料性能",
                technical_details="采用粉末冶金技术,优化复合材料界面结合",
                innovation_points="1.创新复合工艺; 2.提高界面结合强度; 3.降低生产成本25%",
                application_value="应用于电接触材料、导热材料等领域",
                economic_benefit="新增销售额4000万元",
                social_benefit="提高材料利用率30%",
                submission_status=ApplicationStatus.APPROVED,
                submission_time=datetime.now() - timedelta(days=30),
                current_stage="已通过"
            ),
            Application(
                award_cycle_id=1,
                applicant_unit_id=3,
                applicant_user_id=7,
                title="镁合金压铸成型技术创新",
                category="科技进步",
                leader_name="刘经理",
                leader_title="高级工程师",
                team_members="周工,吴工,郑工",
                summary="创新镁合金压铸成型技术,提高产品质量和生产效率",
                technical_details="优化模具设计,改进工艺参数,降低缺陷率",
                innovation_points="1.优化模具结构; 2.控制成型参数; 3.降低缺陷率60%",
                application_value="汽车、3C产品等领域镁合金零部件制造",
                economic_benefit="年产值6000万元",
                social_benefit="轻量化节能,减重25%",
                submission_status=ApplicationStatus.REVIEWING,
                submission_time=datetime.now() - timedelta(days=12),
                current_stage="初审中"
            ),
            Application(
                award_cycle_id=1,
                applicant_unit_id=8,
                applicant_user_id=9,
                title="钛合金3D打印关键技术研发",
                category="技术发明",
                leader_name="孙教授",
                leader_title="教授",
                team_members="赵工,钱工,周工,吴工",
                summary="开发钛合金3D打印关键技术,实现复杂构件制造",
                technical_details="优化激光功率参数,控制组织结构,提高成型质量",
                innovation_points="1.优化打印参数; 2.控制微观组织; 3.提高致密度至99.5%",
                application_value="航空航天、医疗器械等领域复杂零部件制造",
                economic_benefit="新增合同额3000万元",
                social_benefit="缩短研发周期50%,降低材料浪费70%",
                submission_status=ApplicationStatus.SUBMITTED,
                submission_time=datetime.now() - timedelta(days=8),
                current_stage="已提交待推荐"
            )
        ]
        
        for app in new_applications:
            db.add(app)
        db.commit()
        print(f"✓ 添加了 {len(new_applications)} 个申报")
        
        # 5. 添加更多评审
        print("\n5. 添加评审...")
        new_reviews = [
            Review(
                application_id=4,
                expert_id=9,
                scores_json={
                    "技术创新性": 29,
                    "技术先进性": 28,
                    "经济效益": 19,
                    "社会效益": 18
                },
                total_score=94.0,
                comment="技术创新性突出,应用前景广阔,强烈推荐",
                is_anonymous=True,
                status="submitted",
                submitted_at=datetime.now() - timedelta(days=4)
            ),
            Review(
                application_id=4,
                expert_id=10,
                scores_json={
                    "技术创新性": 28,
                    "技术先进性": 29,
                    "经济效益": 18,
                    "社会效益": 19
                },
                total_score=94.0,
                comment="技术方案先进,经济社会效益显著,建议通过",
                is_anonymous=True,
                status="submitted",
                submitted_at=datetime.now() - timedelta(days=2)
            ),
            Review(
                application_id=5,
                expert_id=3,
                scores_json={
                    "技术创新性": 27,
                    "技术先进性": 28,
                    "经济效益": 18,
                    "社会效益": 19
                },
                total_score=92.0,
                comment="技术水平高,应用价值大,同意推荐",
                is_anonymous=True,
                status="submitted",
                submitted_at=datetime.now() - timedelta(days=6)
            )
        ]
        
        for review in new_reviews:
            db.add(review)
        db.commit()
        print(f"✓ 添加了 {len(new_reviews)} 个评审")
        
        # 6. 添加评委会决议
        print("\n6. 添加评委会决议...")
        decisions = [
            CommitteeDecision(
                application_id=6,
                decision_type="approved",
                decision_date=datetime.now() - timedelta(days=5),
                vote_for=8,
                vote_against=0,
                vote_abstain=1,
                decision_content="经评审委员会讨论,该项目技术创新性强,应用效果显著,一致同意通过",
                notes="建议作为一等奖候选项目",
                decided_by=13
            )
        ]
        
        for decision in decisions:
            db.add(decision)
        db.commit()
        print(f"✓ 添加了 {len(decisions)} 个评委会决议")
        
        # 7. 添加更多公示
        print("\n7. 添加公示...")
        new_announcements = [
            Announcement(
                title="2024年度XXXX协会科学技术奖初评结果公示",
                content="根据评审工作安排,现将初评通过项目予以公示,公示期15天,如有异议请在公示期内提出...",
                announcement_type="初评公示",
                start_time=datetime.now() - timedelta(days=10),
                end_time=datetime.now() + timedelta(days=5),
                status="active",
                created_by=1
            )
        ]
        
        for announcement in new_announcements:
            db.add(announcement)
        db.commit()
        print(f"✓ 添加了 {len(new_announcements)} 个公示")
        
        print("\n✓ 扩展演示数据添加完成!")
        print("\n新增账号信息:")
        print("=" * 60)
        print("专家账号: expert04 / expert123, expert05 / expert123")
        print("申报人账号: applicant03 / app123, applicant04 / app123")
        print("\u8bc4委账号: committee02 / comm123")
        print("=" * 60)
        print_statistics(db)
        
    except Exception as e:
        print(f"\n✗ 扩展数据添加失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def print_statistics(db):
    """打印数据统计"""
    print(f"\n当前数据统计:")
    print(f"- 组织: {db.query(Organization).count()} 个")
    print(f"- 用户: {db.query(User).count()} 个")
    print(f"- 奖项: {db.query(Award).count()} 个")
    print(f"- 申报: {db.query(Application).count()} 个")
    print(f"- 评审: {db.query(Review).count()} 个")
    print(f"- 决议: {db.query(CommitteeDecision).count()} 个")
    print(f"- 公示: {db.query(Announcement).count()} 个")
    print("=" * 60)


if __name__ == "__main__":
    print("=" * 60)
    print("XXXX协会科学技术奖评审管理系统 - 扩展演示数据")
    print("=" * 60)
    add_extended_data()
    print("\n数据添加完成,可以继续使用系统!")
