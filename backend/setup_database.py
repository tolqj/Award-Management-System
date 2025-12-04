"""
数据库初始化脚本
Database Setup Script - XXXX协会科学技术奖评审管理系统
"""
import sys
import pymysql
from datetime import datetime, timedelta
from database import engine, Base, SessionLocal
from models import (
    User, Organization, Award, AwardCycle, Application,
    Attachment, Review, CommitteeDecision, Announcement,
    UserRole, OrgType, AwardLevel, ApplicationStatus, DecisionType
)
from crud.user import get_password_hash
from config import settings


def create_database():
    """创建数据库"""
    try:
        conn = pymysql.connect(
            host=settings.DB_HOST,
            port=settings.DB_PORT,
            user=settings.DB_USER,
            password=settings.DB_PASSWORD
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{settings.DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
        print(f"✓ 数据库 '{settings.DB_NAME}' 创建成功")
        conn.close()
    except Exception as e:
        print(f"✗ 数据库创建失败: {e}")
        sys.exit(1)


def create_tables():
    """创建所有表"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✓ 数据库表创建成功")
    except Exception as e:
        print(f"✗ 数据库表创建失败: {e}")
        sys.exit(1)


def init_demo_data():
    """初始化演示数据"""
    db = SessionLocal()
    
    try:
        print("\n开始创建演示数据...")
        
        # 检查是否已有用户数据
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("\n检测到已存在用户数据，跳过演示数据创建")
            print(f"当前数据库已有 {existing_users} 个用户")
            return
        
        # 1. 创建组织
        print("\n1. 创建组织...")
        organizations = [
            Organization(
                name="XXXX协会",
                code="ORG001",
                org_type=OrgType.ASSOCIATION,
                contact_person="李主任",
                contact_phone="010-88888888",
                email="admin@nonferrous.org",
                address="北京市朝阳区"
            ),
            Organization(
                name="XX科学技术研究院",
                code="ORG002",
                org_type=OrgType.INSTITUTE,
                contact_person="张院长",
                contact_phone="010-88888889",
                email="contact@institute.com",
                address="北京市海淀区"
            ),
            Organization(
                name="XX铜业集团有限公司",
                code="ORG003",
                org_type=OrgType.ENTERPRISE,
                contact_person="王总经理",
                contact_phone="0571-88888888",
                email="contact@copper.com",
                address="浙江省杭州市"
            ),
            Organization(
                name="XX矿业大学",
                code="ORG004",
                org_type=OrgType.UNIVERSITY,
                contact_person="赵教授",
                contact_phone="010-88888890",
                email="contact@university.edu",
                address="北京市海淀区"
            ),
            Organization(
                name="XX铝业股份有限公司",
                code="ORG005",
                org_type=OrgType.ENTERPRISE,
                contact_person="刘董事长",
                contact_phone="0371-88888888",
                email="contact@aluminum.com",
                address="河南省郑州市"
            )
        ]
        
        for org in organizations:
            db.add(org)
        db.commit()
        print(f"✓ 创建了 {len(organizations)} 个组织")
        
        # 2. 创建用户
        print("\n2. 创建用户...")
        users = [
            User(
                username="admin",
                password_hash=get_password_hash("admin123"),
                real_name="系统管理员",
                email="admin@system.com",
                mobile="13800138000",
                role=UserRole.ADMIN,
                organization_id=1
            ),
            User(
                username="staff01",
                password_hash=get_password_hash("staff123"),
                real_name="协会工作人员",
                email="staff@nonferrous.org",
                mobile="13800138001",
                role=UserRole.STAFF,
                organization_id=1
            ),
            User(
                username="expert01",
                password_hash=get_password_hash("expert123"),
                real_name="王教授",
                email="expert01@university.edu",
                mobile="13800138002",
                role=UserRole.EXPERT,
                organization_id=4
            ),
            User(
                username="expert02",
                password_hash=get_password_hash("expert123"),
                real_name="李研究员",
                email="expert02@institute.com",
                mobile="13800138003",
                role=UserRole.EXPERT,
                organization_id=2
            ),
            User(
                username="expert03",
                password_hash=get_password_hash("expert123"),
                real_name="赵高工",
                email="expert03@enterprise.com",
                mobile="13800138004",
                role=UserRole.EXPERT,
                organization_id=3
            ),
            User(
                username="applicant01",
                password_hash=get_password_hash("app123"),
                real_name="张工程师",
                email="applicant01@institute.com",
                mobile="13800138005",
                role=UserRole.APPLICANT,
                organization_id=2
            ),
            User(
                username="applicant02",
                password_hash=get_password_hash("app123"),
                real_name="刘经理",
                email="applicant02@copper.com",
                mobile="13800138006",
                role=UserRole.APPLICANT,
                organization_id=3
            ),
            User(
                username="committee01",
                password_hash=get_password_hash("comm123"),
                real_name="陈委员",
                email="committee01@nonferrous.org",
                mobile="13800138007",
                role=UserRole.COMMITTEE,
                organization_id=1
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        print(f"✓ 创建了 {len(users)} 个用户")
        
        # 3. 创建奖项
        print("\n3. 创建奖项...")
        awards = [
            Award(
                name="XXXX协会科学技术奖 - 技术发明奖",
                code="AWARD2024-01",
                level=AwardLevel.INDUSTRY,
                year=2024,
                description="表彰在技术发明方面做出突出贡献的项目",
                application_start=datetime.now() - timedelta(days=30),
                application_end=datetime.now() + timedelta(days=60),
                status="active",
                created_by=1
            ),
            Award(
                name="XXXX协会科学技术奖 - 科技进步奖",
                code="AWARD2024-02",
                level=AwardLevel.INDUSTRY,
                year=2024,
                description="表彰在科技进步方面做出突出贡献的项目",
                application_start=datetime.now() - timedelta(days=30),
                application_end=datetime.now() + timedelta(days=60),
                status="active",
                created_by=1
            )
        ]
        
        for award in awards:
            db.add(award)
        db.commit()
        print(f"✓ 创建了 {len(awards)} 个奖项")
        
        # 4. 创建奖项轮次
        print("\n4. 创建奖项轮次...")
        cycles = [
            AwardCycle(
                award_id=1,
                cycle_name="2024年度第一轮",
                start_date=datetime.now() - timedelta(days=30),
                end_date=datetime.now() + timedelta(days=90),
                rules_json={
                    "max_score": 100,
                    "criteria": [
                        {"name": "技术创新性", "weight": 0.3, "max_score": 30},
                        {"name": "技术先进性", "weight": 0.3, "max_score": 30},
                        {"name": "经济效益", "weight": 0.2, "max_score": 20},
                        {"name": "社会效益", "weight": 0.2, "max_score": 20}
                    ]
                },
                quota=20,
                budget=1000000.0,
                status="active"
            )
        ]
        
        for cycle in cycles:
            db.add(cycle)
        db.commit()
        print(f"✓ 创建了 {len(cycles)} 个奖项轮次")
        
        # 5. 创建申报
        print("\n5. 创建申报...")
        applications = [
            Application(
                award_cycle_id=1,
                applicant_unit_id=2,
                applicant_user_id=6,
                title="高性能铜合金材料关键技术研究及应用",
                category="技术发明",
                leader_name="张工程师",
                leader_title="高级工程师",
                team_members="李工,王工,赵工",
                summary="本项目针对高性能铜合金材料开发,解决了关键技术难题,实现了产业化应用",
                technical_details="创新性开发了新型铜合金成分设计方法,突破了高强高导铜合金制备关键技术",
                innovation_points="1.创新性设计了新型合金成分体系; 2.突破了关键制备工艺; 3.建立了完整的产业化生产线",
                application_value="可广泛应用于电子、通信、交通等领域,市场前景广阔",
                economic_benefit="近三年新增销售额5000万元,利润1000万元",
                social_benefit="降低能耗20%,减少排放30%,促进产业升级",
                submission_status=ApplicationStatus.EXPERT_REVIEW,
                submission_time=datetime.now() - timedelta(days=20),
                current_stage="专家评审中"
            ),
            Application(
                award_cycle_id=1,
                applicant_unit_id=3,
                applicant_user_id=7,
                title="铝合金表面处理新技术及工业化应用",
                category="科技进步",
                leader_name="刘经理",
                leader_title="高级工程师",
                team_members="孙工,周工",
                summary="开发了环保型铝合金表面处理新技术,实现了工业化应用",
                technical_details="研发了新型环保表面处理剂,优化了处理工艺参数",
                innovation_points="1.开发了环保型处理剂配方; 2.优化了工艺流程; 3.降低了生产成本",
                application_value="可应用于汽车、建筑等领域的铝合金表面处理",
                economic_benefit="近三年新增销售额3000万元",
                social_benefit="减少有害物质排放50%",
                submission_status=ApplicationStatus.SUBMITTED,
                submission_time=datetime.now() - timedelta(days=15),
                current_stage="已提交待推荐"
            ),
            Application(
                award_cycle_id=1,
                applicant_unit_id=2,
                applicant_user_id=6,
                title="稀土永磁材料制备新工艺研究",
                category="技术发明",
                leader_name="张工程师",
                leader_title="高级工程师",
                team_members="郑工,吴工,冯工",
                summary="开发了稀土永磁材料制备新工艺,提高了材料性能和生产效率",
                technical_details="创新性设计了快速凝固工艺,优化了热处理参数",
                innovation_points="1.开发了快速凝固技术; 2.优化了组织控制方法; 3.提高了磁性能20%",
                application_value="应用于电机、传感器等领域",
                economic_benefit="新增销售额2000万元",
                social_benefit="提高能源利用效率15%",
                submission_status=ApplicationStatus.DRAFT,
                current_stage="草稿"
            )
        ]
        
        for app in applications:
            db.add(app)
        db.commit()
        print(f"✓ 创建了 {len(applications)} 个申报")
        
        # 6. 创建评审
        print("\n6. 创建评审...")
        reviews = [
            Review(
                application_id=1,
                expert_id=3,
                scores_json={
                    "技术创新性": 28,
                    "技术先进性": 27,
                    "经济效益": 18,
                    "社会效益": 18
                },
                total_score=91.0,
                comment="该项目技术创新性强,应用价值高,建议通过",
                is_anonymous=True,
                status="submitted",
                submitted_at=datetime.now() - timedelta(days=5)
            ),
            Review(
                application_id=1,
                expert_id=4,
                scores_json={
                    "技术创新性": 27,
                    "技术先进性": 28,
                    "经济效益": 17,
                    "社会效益": 19
                },
                total_score=91.0,
                comment="技术方案合理,经济社会效益显著,同意通过",
                is_anonymous=True,
                status="submitted",
                submitted_at=datetime.now() - timedelta(days=3)
            )
        ]
        
        for review in reviews:
            db.add(review)
        db.commit()
        print(f"✓ 创建了 {len(reviews)} 个评审")
        
        # 更新申报的评分汇总
        app1 = db.query(Application).filter(Application.id == 1).first()
        if app1:
            app1.score_summary_json = {
                "average_score": 91.0,
                "review_count": 2,
                "scores": [91.0, 91.0],
                "max_score": 91.0,
                "min_score": 91.0
            }
            db.commit()
        
        # 7. 创建公示
        print("\n7. 创建公示...")
        announcements = [
            Announcement(
                title="2024年度XXXX协会科学技术奖拟获奖项目公示",
                content="根据《XXXX协会科学技术奖评审办法》,经专家评审和评审委员会审定,现将2024年度拟获奖项目予以公示...",
                announcement_type="获奖公示",
                start_time=datetime.now(),
                end_time=datetime.now() + timedelta(days=15),
                status="active",
                created_by=1
            )
        ]
        
        for announcement in announcements:
            db.add(announcement)
        db.commit()
        print(f"✓ 创建了 {len(announcements)} 个公示")
        
        print("\n✓ 演示数据创建完成!")
        print("\n默认账号信息:")
        print("=" * 60)
        print("管理员账号: admin / admin123")
        print("工作人员账号: staff01 / staff123")
        print("专家账号: expert01 / expert123, expert02 / expert123")
        print("申报人账号: applicant01 / app123, applicant02 / app123")
        print("评委账号: committee01 / comm123")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ 演示数据创建失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()


def main():
    """主函数"""
    print("=" * 60)
    print("XXXX协会科学技术奖评审管理系统 - 数据库初始化")
    print("=" * 60)
    
    # 1. 创建数据库
    print("\n步骤 1: 创建数据库")
    create_database()
    
    # 2. 创建表
    print("\n步骤 2: 创建数据库表")
    create_tables()
    
    # 3. 初始化演示数据
    print("\n步骤 3: 初始化演示数据")
    init_demo_data()
    
    print("\n" + "=" * 60)
    print("数据库初始化完成!")
    print("=" * 60)
    print("\n现在可以启动应用:")
    print("  python main.py")
    print("\n或访问 API 文档:")
    print("  http://localhost:8000/docs")
    print("=" * 60)


if __name__ == "__main__":
    main()
