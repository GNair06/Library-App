<template>
    <div class="container">
      <h1><i><b>{{ book.title }}</b></i></h1>
      <h3><i>by <b>{{ book.author }}</b></i></h3><br>
      <div><i>{{ book.content }}</i></div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        book: {
          title: '',
          author: '',
          content: ''
        }
      };
    },
    mounted() {
      const id = this.$route.params.id;
      this.fetchBookData(id);
    },
    methods: {
      async fetchBookData(id) {
        const token = localStorage.getItem('access_token');
  
        if (!token) {
          console.error('Error: No access token found.');
          return;
        }
  
        try {
          const response = await fetch(`http://127.0.0.1:5000/view_book_content/${id}`, {
            method: 'GET',
            headers: {
              'Authorization': 'Bearer ' + token,
              'Content-Type': 'application/json',
            },
          });
  
          if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
          }
  
          const data = await response.json();
          this.book = data.book;
        } catch (error) {
          console.error('Error:', error);
        }
      }
    }
  };
  </script>
  
  
  