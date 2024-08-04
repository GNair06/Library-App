<template>
    <div class="container">
      <form @submit.prevent="EditBook" class="mt-3">
        <div class="mb-3">
          <label for="title" class="form-label">Book Title:</label>
          <input v-model="title" type="text" id="title" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="author" class="form-label">Author:</label>
          <input v-model="author" type="text" id="author" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="content" class="form-label">Content:</label>
          <input v-model="content" type="text" id="content" class="form-control" required />
        </div>
        <div class="mb-3">
          <label for="pages" class="form-label">Pages:</label>
          <input v-model="pages" type="number" id="pages" class="form-control" required />
        </div>
        <button type="submit" class="btn btn-primary">submit</button>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        title: '',
        author: '',
        content: '',
        pages: null,
      };
    },
    mounted() {
      const id = this.$route.params.id;
      this.book_data(id);
    },
    methods: {
      book_data(id) {
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          console.error('Error');
          return;
        }
  
        fetch(`http://127.0.0.1:5000/book/${id}`, {
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
            this.title = data.book.title;
            this.author = data.book.author;
            this.content = data.book.content;
            this.pages = data.book.pages;
          })
          .catch(error => {
            console.error(`Error:`, error);
          });
      },
      EditBook() {
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          console.error('Error');
          return;
        }
  
        const id = this.$route.params.id;
  
        fetch(`http://127.0.0.1:5000/edit_book/${id}`, {
          method: 'PUT',
          headers: {
            'Authorization': 'Bearer ' + token,
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            title: this.title,
            author: this.author,
            content: this.content,
            pages: this.pages,
          }),
        })
        .then(response => response.json())
        .then(data => {
          alert(data.message);
            this.$router.push('/view_all_books');
        })
          .catch(error => {
          console.error('Error:', error);
        });
      },
    },
  };
  </script>