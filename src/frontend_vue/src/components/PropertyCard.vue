<template>
  <div :class="['box p-0', { selected: isSelected }]">
    <div class="card-image">
      <figure class="image is-4by3">
        <img :src="currentImage" alt="Property Image" class="property-image" />
        <p class="price-tag">{{ property.price }} Kč/m</p>
        <button @click.stop="prevImage" class="nav-button left-button">
          <i class="fa-solid fa-chevron-left"></i>
        </button>
        <button @click.stop="nextImage" class="nav-button right-button">
          <i class="fa-solid fa-chevron-right"></i>
        </button>
      </figure>
    </div>

    <div class="content p-2">
      <p class="is-size-5 has-text-weight-semibold mb-1">{{ property.name }}</p>
      <div class="grid is-col-min-3 is-gap-0.5 mb-2">
        <span class="cell tag is-light">
          <span class="icon">
            <i class="fa-solid fa-house"></i>
          </span>
          <span class="has-text-weight-bold">{{ property.prop_type }}</span>
        </span>
        <span class="cell tag is-light">
          <span class="icon">
            <i class="fa-solid fa-bed"></i>
          </span>
          <span class="has-text-weight-bold">{{ property.prop_size_kk }}+kk</span>
        </span>
        <span class="cell tag is-light">
          <span class="icon">
            <i class="fa-solid fa-expand"></i>
          </span>
          <span class="has-text-weight-bold">{{ property.prop_size_m2 }}m2</span>
        </span>

        <span class="cell tag is-success">
          <span class="icon">
            <i class="fa-solid fa-seedling"></i>
          </span>
          <span class="has-text-weight-bold">{{ property.energy_class }}</span>
        </span>
        <span class="tag is-info" v-if="property.rk">
          <span class="has-text-weight-bold">RK</span>
        </span>
        <span class="tag is-light">
          <span class="icon">
            <i class="fa-solid fa-stairs"></i>
          </span>
          <span class="has-text-weight-bold">{{ property.floor }}</span>
        </span>

        <span class="tag is-light" v-if="property.parking > 0">
          <span class="icon">
            <i class="fa-solid fa-square-parking"></i>
          </span>
          <span class="has-text-weight-bold">{{ property.parking }}</span>
        </span>

        <span class="tag is-light" v-if="property.elevator">
          <span class="icon">
            <i class="fa-solid fa-elevator"></i>
          </span>
        </span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PropertyCard',
  props: {
    property: {
      type: Object,
      required: true
    },
    isSelected: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      currentImageIndex: 0
    }
  },
  computed: {
    currentImage() {
      return this.property.images[this.currentImageIndex]
    }
  },
  methods: {
    prevImage(event) {
      event.stopPropagation()
      if (this.currentImageIndex > 0) {
        this.currentImageIndex--
      } else {
        this.currentImageIndex = this.property.images.length - 1
      }
    },
    nextImage(event) {
      event.stopPropagation()
      if (this.currentImageIndex < this.property.images.length - 1) {
        this.currentImageIndex++
      } else {
        this.currentImageIndex = 0
      }
    }
  }
}
</script>

<style scoped>
.box {
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  transition:
    background-color 0.3s,
    color 0.3s;
}

.box.selected {
  background-color: rgb(255, 170, 251);
  padding: 0px 0px 0px 0px;
  cursor: pointer;
}

.card-image {
  position: relative;
}

.price-tag {
  position: absolute;
  bottom: 10px;
  right: 10px;
  background-color: rgba(255, 255, 255, 0.95);
  color: rgb(34, 34, 34);
  padding: 5px 10px;
  border-radius: 5px;
  font-size: 1.2em;
  font-weight: bold;
}

.nav-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: rgba(255, 255, 255, 0.9);
  color: rgb(24, 24, 24);
  border: none;
  padding: 10px;
  cursor: pointer;
  font-size: 1.2em;
  border-radius: 20px;
  opacity: 0;
  transition: opacity 0.3s;
}

.card-image:hover .nav-button {
  opacity: 1;
}

.left-button {
  left: 10px;
}

.right-button {
  right: 10px;
}
</style>
