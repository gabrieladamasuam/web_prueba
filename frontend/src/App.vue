<script setup>
import { ref, onMounted } from "vue";
import api from "./services/api.js";

const text = ref("");
const items = ref([]);

async function loadItems() {
  try {
    const res = await api.get("/items");
    items.value = res.data;
  } catch {
    console.error("No se pudo conectar al backend.");
  }
}

async function addItem() {
  if (!text.value) return;
  await api.post("/items", { text: text.value });
  text.value = "";
  loadItems();
}

onMounted(loadItems);
</script>

<template>
  <main>
    <h1>Mini App — Pruebas Cloud</h1>

    <div class="input-row">
      <input v-model="text" placeholder="Nuevo item" />
      <button @click="addItem">Añadir</button>
    </div>

    <ul>
      <li v-for="item in items" :key="item.id">
        {{ item.text }}
      </li>
    </ul>
  </main>
</template>

<style>
main {
  max-width: 500px;
  margin: auto;
  padding: 20px;
  font-family: sans-serif;
}

.input-row {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

input {
  flex: 1;
  padding: 8px;
  font-size: 16px;
}

button {
  padding: 8px 12px;
  font-size: 16px;
  cursor: pointer;
}
</style>

