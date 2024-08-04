<template>
  <div>
    <form @submit.prevent="submitForm">
      <label for="sectionName" style="color: peru;"><b>Section Name:</b></label><br><br>
      <input type="text" id="sectionName" v-model="sectionName" required><br><br>
      <button type="submit" style="background-color: antiquewhite;">Submit</button><br><br>
    </form>
    <div v-if="sectionId">
      <router-link :to="`/books_of_section/${sectionId}`">
        <b><p style="padding: 10px; color: peru; font-size: 30px;">Click here to view books</p></b>
      </router-link>
    </div>
    <div v-if="errorMessage">
      <p>{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      sectionName: '',
      sectionId: null,
      errorMessage: ''
    };
  },
  methods: {
    async submitForm() {
  try {
    const response = await fetch('http://localhost:5000/section_form', { // Update the URL with your Flask server address
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ sectionName: this.sectionName })
    });
    const data = await response.json();
    if (response.ok) {
      this.sectionId = data.section_id;
      this.errorMessage = '';
    } else {
      this.sectionId = null;
      this.errorMessage = data.message || 'An error occurred.';
    }
  } catch (error) {
    console.error('Error:', error);
    this.sectionId = null;
    this.errorMessage = 'An error occurred.';
  }
}
  }
};
</script>
