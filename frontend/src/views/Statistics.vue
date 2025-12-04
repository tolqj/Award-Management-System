<template>
  <div class="statistics-container">
    <!-- 概览卡片 -->
    <el-row :gutter="20" class="overview-row">
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background: #409eff">
              <el-icon :size="32"><Document /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">申报总数</div>
              <div class="stat-value">{{ overview.total_applications }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background: #67c23a">
              <el-icon :size="32"><Check /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">已通过</div>
              <div class="stat-value">{{ overview.approved }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background: #e6a23c">
              <el-icon :size="32"><Clock /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">评审中</div>
              <div class="stat-value">{{ overview.reviewing }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-item">
            <div class="stat-icon" style="background: #f56c6c">
              <el-icon :size="32"><Close /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-label">未通过</div>
              <div class="stat-value">{{ overview.rejected }}</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 图表区域 -->
    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-weight: bold;">申报状态分布</span>
            </div>
          </template>
          <div ref="statusChartRef" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="never">
          <template #header>
            <div style="display: flex; justify-content: space-between; align-items: center;">
              <span style="font-weight: bold;">年度申报趋势</span>
            </div>
          </template>
          <div ref="trendChartRef" style="width: 100%; height: 350px"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 数据导出 -->
    <el-card shadow="never" style="margin-top: 20px">
      <template #header>
        <span style="font-weight: bold;">数据导出</span>
      </template>
      <el-space>
        <el-button type="primary" @click="exportApplications">
          <el-icon><Download /></el-icon>
          <span>导出申报数据</span>
        </el-button>
        <el-button type="success" @click="exportStatistics">
          <el-icon><Download /></el-icon>
          <span>导出统计报表</span>
        </el-button>
      </el-space>
    </el-card>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Document, Check, Clock, Close, Download } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { statisticsAPI } from '@/api'

const statusChartRef = ref(null)
const trendChartRef = ref(null)
let statusChart = null
let trendChart = null

const overview = ref({
  total_applications: 0,
  approved: 0,
  reviewing: 0,
  rejected: 0
})

const statusData = ref([])
const trendData = ref({ years: [], counts: [] })

const fetchOverview = async () => {
  try {
    const data = await statisticsAPI.overview()
    overview.value = data
  } catch (error) {
    ElMessage.error('获取概览数据失败')
  }
}

const fetchStatusData = async () => {
  try {
    const data = await statisticsAPI.byStatus()
    statusData.value = data
    renderStatusChart()
  } catch (error) {
    ElMessage.error('获取状态分布数据失败')
  }
}

const fetchTrendData = async () => {
  try {
    const data = await statisticsAPI.byYear()
    trendData.value = data
    renderTrendChart()
  } catch (error) {
    ElMessage.error('获取趋势数据失败')
  }
}

const renderStatusChart = () => {
  if (!statusChartRef.value) return
  
  if (statusChart) {
    statusChart.dispose()
  }
  
  statusChart = echarts.init(statusChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        type: 'pie',
        radius: '60%',
        data: statusData.value,
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        }
      }
    ]
  }
  
  statusChart.setOption(option)
}

const renderTrendChart = () => {
  if (!trendChartRef.value) return
  
  if (trendChart) {
    trendChart.dispose()
  }
  
  trendChart = echarts.init(trendChartRef.value)
  
  const option = {
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: trendData.value.years || []
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '申报数量',
        type: 'line',
        data: trendData.value.counts || [],
        smooth: true,
        itemStyle: {
          color: '#409eff'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(64, 158, 255, 0.4)' },
              { offset: 1, color: 'rgba(64, 158, 255, 0.1)' }
            ]
          }
        }
      }
    ]
  }
  
  trendChart.setOption(option)
}

const exportApplications = async () => {
  try {
    const blob = await statisticsAPI.exportApplications()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `申报数据_${new Date().toISOString().split('T')[0]}.xlsx`
    a.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

const exportStatistics = async () => {
  try {
    const blob = await statisticsAPI.exportStatistics()
    const url = window.URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = `统计报表_${new Date().toISOString().split('T')[0]}.xlsx`
    a.click()
    window.URL.revokeObjectURL(url)
    ElMessage.success('导出成功')
  } catch (error) {
    ElMessage.error('导出失败')
  }
}

onMounted(() => {
  fetchOverview()
  fetchStatusData()
  fetchTrendData()
  
  window.addEventListener('resize', () => {
    statusChart?.resize()
    trendChart?.resize()
  })
})

onUnmounted(() => {
  statusChart?.dispose()
  trendChart?.dispose()
})
</script>

<style scoped>
.statistics-container {
  padding: 0;
}

.overview-row {
  margin-bottom: 0;
}

.stat-card {
  border-radius: 8px;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
}
</style>
