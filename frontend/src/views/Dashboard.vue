<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ statistics.total_applications }}</div>
            <div class="stat-label">申报总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ statistics.total_organizations }}</div>
            <div class="stat-label">组织总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ statistics.total_experts }}</div>
            <div class="stat-label">专家总数</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-item">
            <div class="stat-value">{{ statistics.total_reviews }}</div>
            <div class="stat-label">评审总数</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card>
          <template #header>
            <div>申报状态分布</div>
          </template>
          <div ref="statusChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <template #header>
            <div>组织类型分布</div>
          </template>
          <div ref="orgChartRef" style="height: 300px"></div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { statisticsAPI } from '@/api'
import * as echarts from 'echarts'

const statistics = ref({
  total_applications: 0,
  total_organizations: 0,
  total_experts: 0,
  total_reviews: 0,
  application_by_status: {},
  application_by_org_type: {}
})

const statusChartRef = ref(null)
const orgChartRef = ref(null)

const fetchStatistics = async () => {
  const data = await statisticsAPI.overview()
  statistics.value = data
  await nextTick()
  initCharts()
}

const initCharts = () => {
  if (statusChartRef.value) {
    const chart = echarts.init(statusChartRef.value)
    const statusData = Object.entries(statistics.value.application_by_status).map(([name, value]) => ({
      name,
      value
    }))
    
    chart.setOption({
      tooltip: { trigger: 'item' },
      legend: { orient: 'vertical', left: 'left' },
      series: [{
        type: 'pie',
        radius: '50%',
        data: statusData
      }]
    })
  }

  if (orgChartRef.value) {
    const chart = echarts.init(orgChartRef.value)
    const orgData = Object.entries(statistics.value.application_by_org_type).map(([name, value]) => ({
      name,
      value
    }))
    
    chart.setOption({
      tooltip: { trigger: 'item' },
      legend: { orient: 'vertical', left: 'left' },
      series: [{
        type: 'pie',
        radius: '50%',
        data: orgData
      }]
    })
  }
}

onMounted(() => {
  fetchStatistics()
})
</script>

<style scoped>
.stat-card {
  text-align: center;
}

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 10px;
}

.stat-label {
  font-size: 14px;
  color: #666;
}
</style>
