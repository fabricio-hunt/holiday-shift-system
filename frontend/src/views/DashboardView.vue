<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../services/api'
import { LogOut, Plus, Trash2, Calendar, User, LayoutDashboard, Search } from 'lucide-vue-next'

const authStore = useAuthStore()
const shifts = ref([])
const isLoading = ref(true)
const isSubmitting = ref(false)

// Form Data
const newShift = ref({
  name: '',
  collaborator_name: '',
  registration_number: '',
  holiday_date: ''
})

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

const handleAddShift = async () => {
  if (!newShift.value.name || !newShift.value.holiday_date) return
  
  try {
    isSubmitting.value = true
    await api.post('/shifts', newShift.value)
    await fetchShifts() // Refresh list
    // Reset form
    newShift.value.name = ''
    newShift.value.collaborator_name = ''
    newShift.value.registration_number = ''
    newShift.value.holiday_date = ''
  } catch (error) {
    console.error('Failed to add shift', error)
    alert('Failed to add holiday shift')
  } finally {
    isSubmitting.value = false
  }
}

const handleDeleteShift = async (id) => {
  if (!confirm('Tem certeza que deseja excluir esta escala?')) return
  
  try {
    await api.delete(`/shifts/${id}`)
    shifts.value = shifts.value.filter(s => s.id !== id)
  } catch (error) {
    console.error('Failed to delete shift', error)
    alert('Erro ao excluir escala')
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

onMounted(() => {
  fetchShifts()
})
</script>

<template>
  <div class="dashboard-layout">
    <!-- Sidebar / Navigation -->
    <aside class="sidebar">
      <div class="brand">
        <LayoutDashboard class="icon" />
        <span>Gestão de Escala</span>
      </div>
      
      <nav class="nav-links">
        <a href="#" class="nav-item active">
          <Calendar class="icon" />
          <span>Feriados & Colaboradores</span>
        </a>
      </nav>

      <div class="user-profile">
        <div class="user-info">
          <User class="icon" />
          <span class="username">{{ authStore.user?.email }}</span>
        </div>
        <button @click="authStore.logout" class="logout-btn" title="Logout">
          <LogOut class="icon" />
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="main-content">
      <header class="top-bar">
        <h1>Colaboradores Cadastrados</h1>
        <div class="search-bar">
            <!-- Search placeholder -->
            <Search class="icon search-icon" />
            <input type="text" placeholder="Buscar..." class="search-input" />
        </div>
      </header>

      <div class="content-wrapper">
        
        <!-- Add Shift Card -->
        <div class="glass-card add-shift-card">
          <h2>Adicionar Nova Escala</h2>
          <form @submit.prevent="handleAddShift" class="add-form">
            <div class="form-row">
              <div class="form-group">
                <label>Nome do Feriado</label>
                <input 
                  type="text" 
                  v-model="newShift.name" 
                  placeholder="ex: Natal"
                  required
                >
              </div>
              <div class="form-group">
                <label>Nome do Colaborador</label>
                <input 
                  type="text" 
                  v-model="newShift.collaborator_name" 
                  placeholder="Nome Completo"
                  required
                >
              </div>
              <div class="form-group">
                <label>Matrícula</label>
                <input 
                  type="text" 
                  v-model="newShift.registration_number" 
                  placeholder="12345"
                  required
                >
              </div>
              <div class="form-group">
                <label>Data</label>
                <input 
                  type="date" 
                  v-model="newShift.holiday_date" 
                  required
                >
              </div>
              <div class="form-actions">
                <button type="submit" class="btn" :disabled="isSubmitting">
                  <Plus class="icon" size="18" />
                  <span>{{ isSubmitting ? 'Adicionando...' : 'Adicionar' }}</span>
                </button>
              </div>
            </div>
          </form>
        </div>

        <!-- Shift List -->
        <div class="shifts-grid">
            <div v-if="isLoading" class="loading-state">
                Carregando...
            </div>
            <div v-else-if="shifts.length === 0" class="empty-state">
                <Calendar class="icon-lg" />
                <p>Nenhuma escala encontrada.</p>
            </div>
            
            <div v-else class="shift-card glass-card" v-for="shift in shifts" :key="shift.id">
                <div class="shift-content">
                    <div class="shift-header">
                        <h3>{{ shift.name }}</h3>
                        <div class="shift-meta">
                            <span class="collaborator">{{ shift.collaborator_name }} ({{ shift.registration_number }})</span>
                            <span class="shift-date">{{ formatDate(shift.holiday_date) }}</span>
                        </div>
                    </div>
                </div>
                <button @click="handleDeleteShift(shift.id)" class="delete-btn" title="Delete">
                    <Trash2 size="18" />
                </button>
            </div>
        </div>

      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

/* Sidebar */
.sidebar {
  width: 260px;
  background: var(--color-surface);
  border-right: 1px solid var(--color-border);
  display: flex;
  flex-direction: column;
  padding: 1.5rem;
  position: fixed;
  height: 100vh;
  z-index: 10;
}

.brand {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  font-weight: 800;
  color: var(--color-primary);
  margin-bottom: 3rem;
}

.nav-links {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  color: var(--color-text-muted);
  text-decoration: none;
  border-radius: var(--radius-md);
  transition: all 0.2s;
}

.nav-item:hover, .nav-item.active {
  background: rgba(56, 189, 248, 0.1);
  color: var(--color-primary);
}

.user-profile {
  border-top: 1px solid var(--color-border);
  padding-top: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
  color: var(--color-text);
  overflow: hidden;
}

.username {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 120px;
}

.logout-btn {
  background: transparent;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: var(--radius-md);
  transition: color 0.2s;
}

.logout-btn:hover {
  color: var(--color-error);
  background: rgba(239, 68, 68, 0.1);
}

/* Main Content */
.main-content {
  flex: 1;
  margin-left: 260px;
  padding: 2rem;
}

.top-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 2rem;
}

.top-bar h1 {
    font-size: 1.75rem;
    font-weight: 700;
}

.search-bar {
    position: relative;
    width: 300px;
}

.search-input {
    padding-left: 2.5rem;
    margin-bottom: 0;
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

.content-wrapper {
    max-width: 1000px;
    margin: 0 auto;
}

/* Add Shift Card */
.add-shift-card {
    margin-bottom: 2rem;
    padding: 1.5rem;
}

.add-shift-card h2 {
    font-size: 1.25rem;
    margin-bottom: 1rem;
}

.add-form .form-row {
    display: grid;
    grid-template-columns: 2fr 2fr 1fr 1fr auto;
    gap: 1rem;
    align-items: flex-end;
}

.add-form .form-group {
    flex: 1;
}

.add-form .form-group label {
    margin-bottom: 0.25rem;
}

.add-form .form-group input {
    margin-bottom: 0;
}

.add-form .form-actions {
    padding-bottom: 2px;
}

/* Shifts Grid */
.shifts-grid {
    display: grid;
    gap: 1rem;
}

.shift-card {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.25rem;
    transition: transform 0.2s, box-shadow 0.2s;
}

.shift-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
    border-color: var(--color-primary);
}

.shift-header h3 {
    font-size: 1.1rem;
    margin-bottom: 0.25rem;
    color: var(--color-primary);
}

.shift-meta {
    display: flex;
    gap: 1rem;
    font-size: 0.9rem;
    color: var(--color-text-muted);
}

.collaborator {
    color: var(--color-text);
    font-weight: 500;
}

.shift-date {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.delete-btn {
    background: transparent;
    border: none;
    color: var(--color-text-muted);
    cursor: pointer;
    padding: 0.5rem;
    border-radius: var(--radius-md);
    transition: all 0.2s;
}

.delete-btn:hover {
    color: var(--color-error);
    background: rgba(239, 68, 68, 0.1);
}

.empty-state {
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
    width: 20px; 
    height: 20px;
}
</style>
