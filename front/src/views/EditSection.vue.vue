<template>
    <div class="container">
      <form @submit.prevent="EditSection" class="mt-3">
        <div class="mb-3">
          <label for="name" class="form-label">Section Name:</label>
          <input v-model="name" type="text" id="name" class="form-control" required />
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
    mounted() {
      const id = this.$route.params.id;
      this.section_data(id);
    },
    methods: {
      section_data(id) {
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          console.error('Error');
          return;
        }
  
        fetch(`http://127.0.0.1:5000/section/${id}`, {
          method: 'GET',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
          },
        })
          .then(response => {
            return response.json();
          })
          .then(data => {
            this.name = data.section.name;
          })
          .catch(error => {
            console.error(`Error:`, error);
          });
      },
      EditSection() {
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          console.error('Error');
          return;
        }
  
        const id = this.$route.params.id;
  
        fetch(`http://127.0.0.1:5000/edit_section/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: this.name,
          }),
        })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
            this.$router.push('/view_all_sections');
        })
          .catch(error => {
          console.error('Error:', error);
        });
      },
    },
  };
  </script>
  