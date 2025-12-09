<script setup>
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const error = ref('')
const isLoading = ref(false)

const authStore = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  error.value = ''
  isLoading.value = true
  
  try {
    await authStore.login(email.value, password.value)
    router.push('/admin')
  } catch (err) {
    console.error(err)
    error.value = 'Credenciais Inválidas'
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <div class="login-wrapper">
    <div class="glass-card login-card">
      <h1 class="login-title">Bem-vindo</h1>
      <p class="login-subtitle">Entre para gerenciar a escala</p>
      
      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="email">Email</label>
          <input 
            type="email" 
            id="email" 
            v-model="email" 
            placeholder="nome@empresa.com.br" 
            required
            autocomplete="email"
          >
        </div>
        
        <div class="form-group">
          <label for="password">Senha</label>
          <input 
            type="password" 
            id="password" 
            v-model="password" 
            placeholder="••••••••" 
            required
            autocomplete="current-password"
          >
        </div>
        
        <div v-if="error" class="error-msg">
          {{ error }}
        </div>
        
        <button type="submit" class="btn btn-primary" :disabled="isLoading">
          <span v-if="isLoading">Entrando...</span>
          <span v-else>Entrar</span>
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 1rem;
}

.login-card {
  width: 100%;
  max-width: 400px;
  padding: 3rem 2rem;
  animation: fadeIn 0.5s ease-out;
}

.login-title {
  font-size: 2rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: 0.5rem;
}

.login-subtitle {
  color: var(--color-text-muted);
  margin-bottom: 2rem;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  text-align: left;
}

.btn-primary {
  width: 100%;
  margin-top: 1rem;
}

.error-msg {
  color: var(--color-error);
  font-size: 0.875rem;
  background: rgba(239, 68, 68, 0.1);
  padding: 0.75rem;
  border-radius: var(--radius-md);
  border: 1px solid rgba(239, 68, 68, 0.2);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
