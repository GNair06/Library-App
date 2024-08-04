<template>
    <div class="container mt-5">
      <h2>Create Section</h2>
      <form @submit.prevent="createSection" class="mt-3">
        <div class="mb-3">
          <label for="name" class="form-label">Section Name</label>
          <input v-model="name" type="text" class="form-control" id="name" required>
        </div>
        <button type="submit" class="btn btn-primary">submit</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        name: '',
      };
    },
    methods: {
      async createSection() {
        try {
          const response = await fetch('http://localhost:5000/create_section', {
            method: 'POST',
            headers: {
              'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({
              name: this.name,
            }),
          });
  
          const data = await response.json();
  
          if (response.ok) {
            alert(data.message);
            // Route for displaying all sections
            this.$router.push('/view_all_sections');
          } else {
            alert('Error: ' + data.error);
          }
        } catch (error) {
          console.error('Error:', error);
          alert('An error has occurred.');
        }
      },
    },
  };
  </script>
