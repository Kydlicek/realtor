<script>
import { ref, onMounted, onBeforeUnmount } from 'vue'

export default {
  setup() {
    const menu = ref('on')
    const menuRef = ref(null)

    function set_menu(val) {
      menu.value = val
      console.log(menu.value)
      if (val === 'on') {
        setTimeout(function () {
          const inputField = document.querySelector('.input.on')
          if (inputField) {
            console.log('focus')
            inputField.focus()
          }
        }, 1) // 1000 milliseconds = 1 second
      }
    }

    function handleClickOutside(event) {
      if (menuRef.value && !menuRef.value.contains(event.target)) {
        set_menu('off')
      }
    }

    onMounted(() => {
      document.addEventListener('click', handleClickOutside)
    })

    onBeforeUnmount(() => {
      document.removeEventListener('click', handleClickOutside)
    })

    return {
      menu,
      set_menu,
      menuRef
    }
  }
}
</script>

<template>
  <div class="container">
    <div ref="menuRef" v-show="menu === 'on'" class="transition-menu fixed-grid has-4-cols box">
      <div class="grid">
        <div class="field cell is-col-span-4">
          <label class="label">Město</label>
          <p class="control has-icons-left">
            <input class="input on" type="text" placeholder="Praha" ref="inputField" />
            <span class="icon is-small is-left">
              <i class="fa-solid fa-magnifying-glass"></i>
            </span>
          </p>
        </div>
        <div class="field cell is-col-span-4">
          <label class="label">Nájem + energie</label>
          <p class="control">
            <input class="input" type="text" placeholder="14 000" />
          </p>
        </div>
        <div class="field cell is-col-span-2">
          <label class="label">místnosti</label>
          <p class="control">
            <input class="input" type="text" placeholder="3" />
          </p>
        </div>
        <div class="field cell is-col-span-2">
          <label class="label">velikost m2</label>
          <p class="control">
            <input class="input" type="text" placeholder="42" />
          </p>
        </div>
        <div @click="set_menu('off')" class="cell is-col-span-4 field">
          <div class="control">
            <button class="button is-link">Vyhledat</button>
          </div>
        </div>
      </div>
    </div>
    <div @click="set_menu('on')" v-show="menu === 'off'" class="field cell is-col-span-4 off">
      <p class="control has-icons-left">
        <input class="input" type="text" placeholder="Praha" />
        <span class="icon is-small is-left">
          <i class="fa-solid fa-magnifying-glass"></i>
        </span>
      </p>
    </div>
  </div>
</template>

<style scoped>
.off {
  margin-left: 20px;
  margin-top: 50px;
  width: 73%;
}
.fixed-grid {
  width: 80%;
}
button {
  width: 100%;
}
.transition-menu {
  transition: opacity 0.5s ease;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
