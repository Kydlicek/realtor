<template>
  <div ref="map" class="map-container"></div>
</template>

<script>
import L from 'leaflet';
import 'leaflet/dist/leaflet.css';
import 'leaflet.markercluster/dist/MarkerCluster.css';
import 'leaflet.markercluster/dist/MarkerCluster.Default.css';
import 'leaflet.markercluster/dist/leaflet.markercluster.js';

import houseIconUrl from '../assets/house-solid.svg';

export default {
  name: 'PropertyMap',
  props: {
    properties: Array,
    selectedProperty: Object
  },
  data() {
    return {
      markers: [],
      map: null,
      markersCluster: null
    };
  },
  watch: {
    properties: {
      handler(newProperties) {
        this.updateMarkers(newProperties);
      },
      deep: true, // Ensures the watcher is triggered even if the properties array changes in a non-reactive way
    },
    selectedProperty(newVal) {
      if (newVal) {
        this.zoomToProperty(newVal);
      }
    },
  },
  mounted() {
    this.initMap();
  },
  methods: {
    initMap() {
      this.map = L.map(this.$refs.map).setView([51.505, -0.09], 13);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution:
          '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(this.map);

      this.markersCluster = L.markerClusterGroup();
      this.map.addLayer(this.markersCluster);

      this.updateMarkers(this.properties);
    },
    updateMarkers(properties) {
      // Clear existing markers
      this.markersCluster.clearLayers();
      this.markers = [];

      properties.forEach((property) => {
        const customIcon = L.divIcon({
          className: 'custom-icon',
          html: `
            <div class="marker-icon-wrapper">
              <img src="${houseIconUrl}" class="house-icon" />
              <div class="price-label">${property.price}</div>
            </div>
          `,
          iconSize: [80, 40],
          iconAnchor: [10, 40]
        });

        const marker = L.marker(property.coordinates, { icon: customIcon }).addTo(this.map);

        this.markersCluster.addLayer(marker);
        this.markers.push({ marker });

        marker.on('click', () => {
          this.$emit('property-selected', property);
        });
      });
    },
    zoomToProperty(property) {
      this.map.setView(property.coordinates, 16);
    },
    outZoomProperty(property) {
      this.map.setView(property.coordinates, 32);
    },
    highlightMarker(index) {
      const { marker } = this.markers[index];
      marker.setZIndexOffset(1000);
    },
    resetMarker(index) {
      const { marker } = this.markers[index];
      marker.setZIndexOffset(0);
    },
    selectProperty(property) {
      this.$emit('property-selected', property);
    }
  }
};
</script>

<style>
.map-container {
  z-index: 1;
  width: 100%;
  height: 100%;
}

.custom-icon .marker-icon-wrapper {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: rgb(255, 255, 255);
  border: 1px solid #d3d3d3;
  border-radius: 8px;
  padding: 4px 8px;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
  font-weight: 700;
  white-space: nowrap;
}

.custom-icon .house-icon {
  width: 16px;
  height: 16px;
  margin-right: 5px;
}
</style>
