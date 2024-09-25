<script>
export default {
  data() {
    return {
      menu: 'off' // Start with the menu in 'off' state
    }
  },
  methods: {
    // Method to set the menu state and handle focus when 'on'
    set_menu(val) {
      this.menu = val
      console.log('Menu is:', this.menu)
      if (val === 'on') {
        // Use $nextTick to ensure the DOM is updated before setting focus
        this.$nextTick(() => {
          const inputField = this.$refs.inputField
          if (inputField) {
            console.log('Focusing input field')
            inputField.focus()
          }
        })
      }
    }
    // Method to close the dropdown when clicking outside
  },
  mounted() {
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  }
}
</script>

<template>
  <div class="container">
    <!-- Dropdown menu, shown when 'menu' is 'on' -->
    <div ref="menuRef" v-show="menu === 'on'" class="transition-menu fixed-grid has-3-cols box">
      <div class="grid">
        <!-- Label on the left, Close button on the right -->

        <label class="label">Město</label>
        <div class="cell is-col-from-end-1 close-button" @click="set_menu('off')">
          <span class="icon">
            <i class="fa fa-times"></i>
          </span>
        </div>

        <!-- Město field with focus on click -->
        <div class="field cell is-col-span-4">
          <p class="control has-icons-left">
            <input class="input on" type="text" placeholder="Praha" ref="inputField" />
            <span class="icon is-small is-left">
              <i class="fa-solid fa-magnifying-glass"></i>
            </span>
          </p>
        </div>

        <!-- Additional fields -->
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

        <!-- Search button to close the dropdown -->
        <div @click="set_menu('off')" class="cell is-col-span-4 field">
          <div class="control">
            <button class="button is-link">Vyhledat</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Input field to toggle the dropdown on click, shown when 'menu' is 'off' -->
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
.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
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
  position: relative;
}

.close-button {
  cursor: pointer;
}

.close-button .icon {
  font-size: 18px;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease;
}

.fade-enter, .fade-leave-to /* .fade-leave-active in <2.1.8 */ {
  opacity: 0;
}
</style>
