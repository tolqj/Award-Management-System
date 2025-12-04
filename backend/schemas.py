"""
Pydantic Schemas - 数据验证模型
Request/Response Models for API
"""
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime
from models import UserRole, OrgType, AwardLevel, ApplicationStatus, DecisionType


# ==================== Token & Auth Schemas ====================
class Token(BaseModel):
    """JWT Token响应"""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token数据"""
    username: Optional[str] = None
    role: Optional[str] = None


class LoginRequest(BaseModel):
    """登录请求"""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)


# ==================== User Schemas ====================
class UserBase(BaseModel):
    """用户基础模型"""
    username: str = Field(..., min_length=3, max_length=50)
    real_name: str = Field(..., min_length=2, max_length=50)
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    role: UserRole = UserRole.APPLICANT
    organization_id: Optional[int] = None


class UserCreate(UserBase):
    """创建用户"""
    password: str = Field(..., min_length=6, description="密码至少6位")
    
    @validator('password')
    def validate_password(cls, v):
        """密码复杂度验证"""
        if len(v) < 6:
            raise ValueError('密码至少6位')
        return v


class UserUpdate(BaseModel):
    """更新用户"""
    real_name: Optional[str] = None
    email: Optional[EmailStr] = None
    mobile: Optional[str] = None
    role: Optional[UserRole] = None
    organization_id: Optional[int] = None
    is_active: Optional[bool] = None


class PasswordChange(BaseModel):
    """修改密码"""
    old_password: str
    new_password: str = Field(..., min_length=6)


class UserResponse(UserBase):
    """用户响应"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    organization: Optional['OrganizationResponse'] = None
    
    class Config:
        from_attributes = True


# ==================== Organization Schemas ====================
class OrganizationBase(BaseModel):
    """组织基础模型"""
    name: str = Field(..., min_length=2, max_length=200)
    code: Optional[str] = None
    org_type: OrgType = OrgType.ENTERPRISE
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    description: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    """创建组织"""
    pass


class OrganizationUpdate(BaseModel):
    """更新组织"""
    name: Optional[str] = None
    org_type: Optional[OrgType] = None
    contact_person: Optional[str] = None
    contact_phone: Optional[str] = None
    email: Optional[EmailStr] = None
    address: Optional[str] = None
    description: Optional[str] = None


class OrganizationResponse(OrganizationBase):
    """组织响应"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Award Schemas ====================
class AwardBase(BaseModel):
    """奖项基础模型"""
    name: str = Field(..., min_length=2, max_length=100)
    code: Optional[str] = None
    level: AwardLevel = AwardLevel.INDUSTRY
    year: int = Field(..., ge=2000, le=2100)
    description: Optional[str] = None
    application_start: Optional[datetime] = None
    application_end: Optional[datetime] = None


class AwardCreate(AwardBase):
    """创建奖项"""
    pass


class AwardUpdate(BaseModel):
    """更新奖项"""
    name: Optional[str] = None
    level: Optional[AwardLevel] = None
    description: Optional[str] = None
    application_start: Optional[datetime] = None
    application_end: Optional[datetime] = None
    status: Optional[str] = None


class AwardResponse(AwardBase):
    """奖项响应"""
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Award Cycle Schemas ====================
class AwardCycleBase(BaseModel):
    """奖项轮次基础模型"""
    award_id: int
    cycle_name: str = Field(..., min_length=2, max_length=100)
    start_date: datetime
    end_date: datetime
    rules_json: Optional[Dict[str, Any]] = None
    quota: Optional[int] = None
    budget: Optional[float] = None


class AwardCycleCreate(AwardCycleBase):
    """创建奖项轮次"""
    pass


class AwardCycleUpdate(BaseModel):
    """更新奖项轮次"""
    cycle_name: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    rules_json: Optional[Dict[str, Any]] = None
    quota: Optional[int] = None
    budget: Optional[float] = None
    status: Optional[str] = None


class AwardCycleResponse(AwardCycleBase):
    """奖项轮次响应"""
    id: int
    status: str
    created_at: datetime
    award: Optional[AwardResponse] = None
    
    class Config:
        from_attributes = True


# ==================== Application Schemas ====================
class ApplicationBase(BaseModel):
    """申报基础模型"""
    award_cycle_id: int
    title: str = Field(..., min_length=2, max_length=200)
    category: Optional[str] = None
    leader_name: Optional[str] = None
    leader_title: Optional[str] = None
    team_members: Optional[str] = None
    summary: Optional[str] = None
    technical_details: Optional[str] = None
    innovation_points: Optional[str] = None
    application_value: Optional[str] = None
    economic_benefit: Optional[str] = None
    social_benefit: Optional[str] = None


class ApplicationCreate(ApplicationBase):
    """创建申报"""
    applicant_unit_id: int


class ApplicationUpdate(BaseModel):
    """更新申报"""
    title: Optional[str] = None
    category: Optional[str] = None
    leader_name: Optional[str] = None
    leader_title: Optional[str] = None
    team_members: Optional[str] = None
    summary: Optional[str] = None
    technical_details: Optional[str] = None
    innovation_points: Optional[str] = None
    application_value: Optional[str] = None
    economic_benefit: Optional[str] = None
    social_benefit: Optional[str] = None


class ApplicationSubmit(BaseModel):
    """提交申报"""
    confirm: bool = True


class ApplicationStatusUpdate(BaseModel):
    """更新申报状态"""
    status: ApplicationStatus
    note: Optional[str] = None


class ApplicationResponse(ApplicationBase):
    """申报响应"""
    id: int
    applicant_unit_id: int
    applicant_user_id: Optional[int] = None
    submission_status: ApplicationStatus
    submission_time: Optional[datetime] = None
    current_stage: Optional[str] = None
    final_result: Optional[str] = None
    score_summary_json: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime
    applicant_unit: Optional[OrganizationResponse] = None
    
    class Config:
        from_attributes = True


# ==================== Attachment Schemas ====================
class AttachmentBase(BaseModel):
    """附件基础模型"""
    filename: str
    file_type: Optional[str] = None
    description: Optional[str] = None


class AttachmentResponse(AttachmentBase):
    """附件响应"""
    id: int
    application_id: int
    filepath: str
    file_size: Optional[int] = None
    uploaded_by: Optional[int] = None
    version: int
    upload_time: datetime
    
    class Config:
        from_attributes = True


# ==================== Review Schemas ====================
class ReviewBase(BaseModel):
    """评审基础模型"""
    application_id: int
    scores_json: Dict[str, Any]
    total_score: Optional[float] = None
    comment: Optional[str] = None


class ReviewCreate(ReviewBase):
    """创建评审"""
    pass


class ReviewUpdate(BaseModel):
    """更新评审"""
    scores_json: Optional[Dict[str, Any]] = None
    total_score: Optional[float] = None
    comment: Optional[str] = None


class ReviewSubmit(BaseModel):
    """提交评审"""
    confirm: bool = True


class ReviewResponse(ReviewBase):
    """评审响应"""
    id: int
    expert_id: int
    is_anonymous: bool
    status: str
    submitted_at: Optional[datetime] = None
    created_at: datetime
    expert: Optional[UserResponse] = None
    
    class Config:
        from_attributes = True


# ==================== Committee Decision Schemas ====================
class CommitteeDecisionBase(BaseModel):
    """评审委员会决议基础模型"""
    application_id: int
    decision: DecisionType
    decision_note: Optional[str] = None
    award_grade: Optional[str] = None
    vote_result: Optional[Dict[str, Any]] = None


class CommitteeDecisionCreate(CommitteeDecisionBase):
    """创建决议"""
    meeting_date: Optional[datetime] = None


class CommitteeDecisionResponse(CommitteeDecisionBase):
    """决议响应"""
    id: int
    meeting_date: Optional[datetime] = None
    decided_by: Optional[int] = None
    created_at: datetime
    application: Optional['ApplicationResponse'] = None
    
    class Config:
        from_attributes = True


# ==================== Announcement Schemas ====================
class AnnouncementBase(BaseModel):
    """公示基础模型"""
    title: str = Field(..., min_length=2, max_length=200)
    content: str
    announcement_type: Optional[str] = None
    start_time: datetime
    end_time: datetime
    attachments_json: Optional[Dict[str, Any]] = None


class AnnouncementCreate(AnnouncementBase):
    """创建公示"""
    pass


class AnnouncementUpdate(BaseModel):
    """更新公示"""
    title: Optional[str] = None
    content: Optional[str] = None
    announcement_type: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    attachments_json: Optional[Dict[str, Any]] = None
    status: Optional[str] = None


class AnnouncementResponse(AnnouncementBase):
    """公示响应"""
    id: int
    status: str
    created_by: Optional[int] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Objection Schemas ====================
class ObjectionBase(BaseModel):
    """异议基础模型"""
    announcement_id: int
    application_id: Optional[int] = None
    objector_name: Optional[str] = None
    objector_contact: Optional[str] = None
    objection_content: str


class ObjectionCreate(ObjectionBase):
    """创建异议"""
    pass


class ObjectionResponse(ObjectionBase):
    """异议响应"""
    id: int
    response: Optional[str] = None
    status: str
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True


# ==================== Statistics Schemas ====================
class StatisticsOverview(BaseModel):
    """统计概览"""
    total_applications: int = 0
    total_organizations: int = 0
    total_experts: int = 0
    total_reviews: int = 0
    application_by_status: Dict[str, int] = {}
    application_by_org_type: Dict[str, int] = {}


class StatisticsResponse(BaseModel):
    """统计响应"""
    data: Dict[str, Any]


# ==================== Common Response ====================
class MessageResponse(BaseModel):
    """通用消息响应"""
    message: str
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    """分页响应"""
    total: int
    page: int
    page_size: int
    items: List[Any]
