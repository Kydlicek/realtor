<script setup>
import { ref } from 'vue'
import { useAuth0 } from '@auth0/auth0-vue';

const menu_clicked = ref('') // Define menu_clicked as a reactive ref

const clicked = () => {
  menu_clicked.value = menu_clicked.value === 'is-active' ? '' : 'is-active'
}

// Auth0 hooks
const { loginWithRedirect, logout, isAuthenticated, user } = useAuth0()

// Login function
const login = () => {
  loginWithRedirect()
}

// Logout function
const handleLogout = () => {
  logout({ returnTo: window.location.origin })
}

</script>

<template>
  <div class="hero-head">
    <nav class="navbar" role="navigation" aria-label="main navigation">
      <div class="navbar-brand">
        <a class="navbar-item" href="http://localhost:5173/">
          <img src="../assets/logo.webp" alt="Simple House Logo">
        </a>

        <!-- Show login or logout button based on authentication state -->
        <a class="navbar-item">
          <button v-if="!isAuthenticated" @click="login">Log in</button>
          <button v-if="isAuthenticated" @click="handleLogout">Log out</button>
        </a>

        <a role="button" @click="clicked" :class="'navbar-burger' + ' ' + menu_clicked" aria-label="menu"
          aria-expanded="false" data-target="navbarBasicExample">
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div id="navbarBasicExample" :class="'navbar-menu' + ' ' + menu_clicked">
        <div class="navbar-start">
          <a class="navbar-item"> <!-- Home --> </a>
        </div>

        <div class="navbar-end">
          <div class="navbar-item">
            <div class="buttons">
              <a class="button is-primary">
                <!-- Optional button or signup -->
              </a>
            </div>
          </div>
          <div class="navbar-item" v-if="isAuthenticated">
            <!-- Display user info if authenticated -->
            <p>Welcome, {{ user.name }}</p>
          </div>
        </div>
      </div>
    </nav>
  </div>
</template>
