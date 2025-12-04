"""
数据库模型定义 - XXXX协会科学技术奖评审管理系统
Database Models for Non-ferrous Metals Technology Award Management System
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, JSON, Float, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base
import enum


# 枚举类型定义
class UserRole(str, enum.Enum):
    """用户角色"""
    ADMIN = "admin"  # 系统管理员
    STAFF = "staff"  # 协会工作人员
    RECOMMENDER = "recommender"  # 推荐单位管理员
    APPLICANT = "applicant"  # 申报单位
    EXPERT = "expert"  # 专家评审
    COMMITTEE = "committee"  # 评审委员会
    PUBLIC = "public"  # 公众


class OrgType(str, enum.Enum):
    """组织类型"""
    ENTERPRISE = "enterprise"  # 企业
    INSTITUTE = "institute"  # 研究院所
    UNIVERSITY = "university"  # 高校
    ASSOCIATION = "association"  # 协会
    OTHER = "other"  # 其他


class AwardLevel(str, enum.Enum):
    """奖项级别"""
    NATIONAL = "national"  # 国家级
    INDUSTRY = "industry"  # 行业级
    PROVINCIAL = "provincial"  # 省级


class ApplicationStatus(str, enum.Enum):
    """申报状态"""
    DRAFT = "draft"  # 草稿
    SUBMITTED = "submitted"  # 已提交
    RECOMMENDED = "recommended"  # 推荐通过
    PRELIMINARY_APPROVED = "preliminary_approved"  # 初审通过
    PRELIMINARY_REJECTED = "preliminary_rejected"  # 初审不通过
    EXPERT_REVIEW = "expert_review"  # 专家评审中
    COMMITTEE_REVIEW = "committee_review"  # 评委会终审中
    APPROVED = "approved"  # 终审通过
    REJECTED = "rejected"  # 终审不通过
    ANNOUNCED = "announced"  # 已公示
    ARCHIVED = "archived"  # 已归档


class DecisionType(str, enum.Enum):
    """决议类型"""
    APPROVED = "approved"  # 通过
    REJECTED = "rejected"  # 不通过
    CONDITIONAL = "conditional"  # 有条件通过
    DEFERRED = "deferred"  # 延期


# 数据库模型定义
class User(Base):
    """用户表"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False, comment="用户名")
    password_hash = Column(String(255), nullable=False, comment="密码哈希")
    real_name = Column(String(50), nullable=False, comment="真实姓名")
    email = Column(String(100), unique=True, index=True, comment="邮箱")
    mobile = Column(String(20), comment="手机号")
    role = Column(Enum(UserRole), default=UserRole.APPLICANT, comment="角色")
    organization_id = Column(Integer, ForeignKey("organizations.id"), comment="所属组织ID")
    is_active = Column(Boolean, default=True, comment="是否激活")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    organization = relationship("Organization", back_populates="users")
    applications = relationship("Application", foreign_keys="Application.applicant_user_id", back_populates="applicant_user")
    reviews = relationship("Review", back_populates="expert")
    logs = relationship("Log", back_populates="user")


class Organization(Base):
    """组织/单位表"""
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), unique=True, nullable=False, comment="单位名称")
    code = Column(String(50), unique=True, index=True, comment="单位代码")
    org_type = Column(Enum(OrgType), default=OrgType.ENTERPRISE, comment="单位类型")
    contact_person = Column(String(50), comment="联系人")
    contact_phone = Column(String(20), comment="联系电话")
    email = Column(String(100), comment="邮箱")
    address = Column(String(255), comment="地址")
    description = Column(Text, comment="简介")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    users = relationship("User", back_populates="organization")
    applications = relationship("Application", foreign_keys="Application.applicant_unit_id", back_populates="applicant_unit")


class Award(Base):
    """奖项表"""
    __tablename__ = "awards"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False, comment="奖项名称")
    code = Column(String(50), unique=True, index=True, comment="奖项代码")
    level = Column(Enum(AwardLevel), default=AwardLevel.INDUSTRY, comment="奖项级别")
    year = Column(Integer, nullable=False, comment="年度")
    description = Column(Text, comment="奖项说明")
    application_start = Column(DateTime, comment="申报开始时间")
    application_end = Column(DateTime, comment="申报结束时间")
    status = Column(String(20), default="active", comment="状态")
    created_by = Column(Integer, ForeignKey("users.id"), comment="创建人ID")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    cycles = relationship("AwardCycle", back_populates="award")


class AwardCycle(Base):
    """奖项轮次表"""
    __tablename__ = "award_cycles"
    
    id = Column(Integer, primary_key=True, index=True)
    award_id = Column(Integer, ForeignKey("awards.id"), nullable=False, comment="奖项ID")
    cycle_name = Column(String(100), nullable=False, comment="轮次名称")
    start_date = Column(DateTime, nullable=False, comment="开始日期")
    end_date = Column(DateTime, nullable=False, comment="结束日期")
    rules_json = Column(JSON, comment="评审规则JSON")
    quota = Column(Integer, comment="名额")
    budget = Column(Float, comment="预算")
    status = Column(String(20), default="active", comment="状态")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    award = relationship("Award", back_populates="cycles")
    applications = relationship("Application", back_populates="award_cycle")


class Application(Base):
    """申报表"""
    __tablename__ = "applications"
    
    id = Column(Integer, primary_key=True, index=True)
    award_cycle_id = Column(Integer, ForeignKey("award_cycles.id"), nullable=False, comment="奖项轮次ID")
    applicant_unit_id = Column(Integer, ForeignKey("organizations.id"), nullable=False, comment="申报单位ID")
    applicant_user_id = Column(Integer, ForeignKey("users.id"), comment="申报人ID")
    
    # 申报内容
    title = Column(String(200), nullable=False, comment="项目/成果名称")
    category = Column(String(50), comment="申报类别")
    leader_name = Column(String(50), comment="项目负责人")
    leader_title = Column(String(50), comment="负责人职称")
    team_members = Column(Text, comment="团队成员")
    summary = Column(Text, comment="项目摘要")
    technical_details = Column(Text, comment="技术详情")
    innovation_points = Column(Text, comment="创新点")
    application_value = Column(Text, comment="应用价值")
    economic_benefit = Column(Text, comment="经济效益")
    social_benefit = Column(Text, comment="社会效益")
    
    # 流程与状态
    submission_status = Column(Enum(ApplicationStatus), default=ApplicationStatus.DRAFT, comment="申报状态")
    submission_time = Column(DateTime, comment="提交时间")
    current_stage = Column(String(50), comment="当前阶段")
    final_result = Column(String(50), comment="最终结果")
    score_summary_json = Column(JSON, comment="评分汇总JSON")
    
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    award_cycle = relationship("AwardCycle", back_populates="applications")
    applicant_unit = relationship("Organization", foreign_keys=[applicant_unit_id], back_populates="applications")
    applicant_user = relationship("User", foreign_keys=[applicant_user_id], back_populates="applications")
    attachments = relationship("Attachment", back_populates="application", cascade="all, delete-orphan")
    recommenders = relationship("Recommender", back_populates="application", cascade="all, delete-orphan")
    reviews = relationship("Review", back_populates="application", cascade="all, delete-orphan")
    committee_decisions = relationship("CommitteeDecision", back_populates="application", cascade="all, delete-orphan")


class Attachment(Base):
    """附件表"""
    __tablename__ = "attachments"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, comment="申报ID")
    filename = Column(String(255), nullable=False, comment="文件名")
    filepath = Column(String(500), nullable=False, comment="文件路径")
    file_type = Column(String(20), comment="文件类型")
    file_size = Column(Integer, comment="文件大小(字节)")
    description = Column(String(255), comment="文件描述")
    uploaded_by = Column(Integer, ForeignKey("users.id"), comment="上传人ID")
    version = Column(Integer, default=1, comment="版本号")
    upload_time = Column(DateTime, default=datetime.now, comment="上传时间")
    
    # 关系
    application = relationship("Application", back_populates="attachments")


class Recommender(Base):
    """推荐单位表"""
    __tablename__ = "recommenders"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, comment="申报ID")
    recommender_unit_id = Column(Integer, ForeignKey("organizations.id"), comment="推荐单位ID")
    recommender_user_id = Column(Integer, ForeignKey("users.id"), comment="推荐人ID")
    recommend_time = Column(DateTime, comment="推荐时间")
    recommend_status = Column(String(20), default="pending", comment="推荐状态")
    recommend_document = Column(String(500), comment="推荐文件路径")
    recommend_opinion = Column(Text, comment="推荐意见")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    application = relationship("Application", back_populates="recommenders")


class Review(Base):
    """专家评审表"""
    __tablename__ = "reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, comment="申报ID")
    expert_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="专家ID")
    scores_json = Column(JSON, comment="各项评分JSON")
    total_score = Column(Float, comment="总分")
    comment = Column(Text, comment="评审意见")
    is_anonymous = Column(Boolean, default=True, comment="是否匿名")
    status = Column(String(20), default="pending", comment="评审状态")
    submitted_at = Column(DateTime, comment="提交时间")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    application = relationship("Application", back_populates="reviews")
    expert = relationship("User", back_populates="reviews")


class CommitteeDecision(Base):
    """评审委员会决议表"""
    __tablename__ = "committee_decisions"
    
    id = Column(Integer, primary_key=True, index=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False, comment="申报ID")
    meeting_date = Column(DateTime, comment="会议日期")
    decision = Column(Enum(DecisionType), comment="决议")
    decision_note = Column(Text, comment="决议说明")
    award_grade = Column(String(50), comment="奖励等级")
    decided_by = Column(Integer, ForeignKey("users.id"), comment="决议人ID")
    vote_result = Column(JSON, comment="投票结果JSON")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    application = relationship("Application", back_populates="committee_decisions")


class Announcement(Base):
    """公示表"""
    __tablename__ = "announcements"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False, comment="公示标题")
    content = Column(Text, nullable=False, comment="公示内容")
    announcement_type = Column(String(50), comment="公示类型")
    start_time = Column(DateTime, nullable=False, comment="开始时间")
    end_time = Column(DateTime, nullable=False, comment="结束时间")
    attachments_json = Column(JSON, comment="附件JSON")
    status = Column(String(20), default="active", comment="状态")
    created_by = Column(Integer, ForeignKey("users.id"), comment="创建人ID")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    objections = relationship("Objection", back_populates="announcement", cascade="all, delete-orphan")


class Objection(Base):
    """异议表"""
    __tablename__ = "objections"
    
    id = Column(Integer, primary_key=True, index=True)
    announcement_id = Column(Integer, ForeignKey("announcements.id"), nullable=False, comment="公示ID")
    application_id = Column(Integer, ForeignKey("applications.id"), comment="相关申报ID")
    objector_name = Column(String(100), comment="异议人姓名")
    objector_contact = Column(String(100), comment="异议人联系方式")
    objection_content = Column(Text, nullable=False, comment="异议内容")
    response = Column(Text, comment="回复")
    status = Column(String(20), default="pending", comment="处理状态")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    # 关系
    announcement = relationship("Announcement", back_populates="objections")


class Log(Base):
    """操作日志表"""
    __tablename__ = "logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), comment="用户ID")
    action_type = Column(String(50), nullable=False, comment="操作类型")
    action_desc = Column(Text, comment="操作描述")
    ip_address = Column(String(50), comment="IP地址")
    user_agent = Column(String(255), comment="用户代理")
    request_data = Column(JSON, comment="请求数据")
    created_at = Column(DateTime, default=datetime.now, comment="创建时间")
    
    # 关系
    user = relationship("User", back_populates="logs")
