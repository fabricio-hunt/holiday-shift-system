<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'
import { Calendar, Search, LogIn, LayoutDashboard } from 'lucide-vue-next'

const router = useRouter()
const shifts = ref([])
const isLoading = ref(true)
const searchQuery = ref('')

const fetchShifts = async () => {
  try {
    isLoading.value = true
    const response = await api.get('/shifts')
    shifts.value = response.data
  } catch (error) {
    console.error('Failed to fetch shifts', error)
  } finally {
    isLoading.value = false
  }
}

const formatDate = (dateString) => {
  return new Date(dateString).toLocaleDateString('pt-BR', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

const filteredShifts = computed(() => {
  if (!searchQuery.value) return shifts.value
  const query = searchQuery.value.toLowerCase()
  return shifts.value.filter(shift => 
    shift.name.toLowerCase().includes(query) || 
    shift.collaborator_name.toLowerCase().includes(query) ||
    shift.registration_number.toLowerCase().includes(query)
  )
})

onMounted(() => {
  fetchShifts()
})
</script>

<template>
  <div class="public-layout">
    <header class="public-header">
      <div class="container header-content">
        <div class="brand">
          <LayoutDashboard class="icon" />
          <span>Gestão de Escala</span>
        </div>
        <button @click="router.push('/login')" class="btn btn-outline">
          <LogIn class="icon" size="18" />
          <span>Área Administrativa</span>
        </button>
      </div>
    </header>

    <main class="container main-content">
      <div class="content-header">
        <h1>Escalas de Feriados</h1>
        <div class="search-bar">
            <Search class="icon search-icon" />
            <input 
              type="text" 
              v-model="searchQuery" 
              placeholder="Buscar por nome, feriado ou matrícula..." 
              class="search-input" 
            />
        </div>
      </div>

      <div class="shifts-grid">
          <div v-if="isLoading" class="loading-state">
              Carregando escalas...
          </div>
          <div v-else-if="filteredShifts.length === 0" class="empty-state">
              <Calendar class="icon-lg" />
              <p>Nenhuma escala encontrada.</p>
          </div>
          
          <div v-else class="shift-card glass-card" v-for="shift in filteredShifts" :key="shift.id">
              <div class="shift-content">
                  <div class="shift-header">
                      <h3>{{ shift.name }}</h3>
                      <div class="shift-meta">
                          <span class="collaborator">{{ shift.collaborator_name }}</span>
                          <span class="registration">Mat: {{ shift.registration_number }}</span>
                      </div>
                  </div>
                  <div class="shift-date-row">
                    <Calendar class="icon-sm" />
                    <span class="shift-date">{{ formatDate(shift.holiday_date) }}</span>
                  </div>
              </div>
          </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.public-layout {
  min-height: 100vh;
  background: var(--color-bg);
}

.public-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: 1rem 0;
  margin-bottom: 2rem;
}

.header-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-primary);
}

.btn-outline {
  background: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text);
  gap: 0.5rem;
}

.btn-outline:hover {
  border-color: var(--color-primary);
  color: var(--color-primary);
  background: rgba(56, 189, 248, 0.1);
}

.main-content {
  padding-bottom: 4rem;
}

.content-header {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  margin-bottom: 2rem;
  text-align: center;
}

.content-header h1 {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text);
}

.search-bar {
  position: relative;
  max-width: 500px;
  width: 100%;
  margin: 0 auto;
}

.search-input {
  padding-left: 2.5rem;
  margin-bottom: 0;
  background: var(--color-surface);
  border-color: var(--color-border);
}

.search-icon {
  position: absolute;
  left: 0.75rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  width: 18px;
  height: 18px;
}

.shifts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.shift-card {
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
  border-top: 4px solid var(--color-primary);
}

.shift-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}

.shift-header h3 {
  font-size: 1.25rem;
  margin-bottom: 0.5rem;
  color: var(--color-text);
}

.shift-meta {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  margin-bottom: 1rem;
}

.collaborator {
  font-weight: 600;
  color: var(--color-primary);
  font-size: 1.1rem;
}

.registration {
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.shift-date-row {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text);
  background: rgba(255, 255, 255, 0.05);
  padding: 0.5rem;
  border-radius: var(--radius-md);
}

.icon-sm {
  width: 16px;
  height: 16px;
  color: var(--color-text-muted);
}

.empty-state {
  grid-column: 1 / -1;
  text-align: center;
  padding: 4rem;
  color: var(--color-text-muted);
}

.icon-lg {
  width: 48px;
  height: 48px;
  margin-bottom: 1rem;
  opacity: 0.5;
}

.icon {
  width: 24px;
  height: 24px;
}
</style>
