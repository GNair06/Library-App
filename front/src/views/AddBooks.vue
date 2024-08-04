<template>
    <div class="container mt-5">
      <div class="card">
        <div class="card-header">
          <h2>Add Book</h2>
        </div>
        <div class="card-body">
          <form @submit.prevent="addBook" class="row g-3">
            <div class="col-md-6">
              <label for="bookTitle" class="form-label">Book Title:</label>
              <input v-model="bookTitle" type="text" class="form-control" id="bookTitle" required />
            </div>
            <div class="col-md-6">
              <label for="author" class="form-label">Author:</label>
              <input v-model="author" type="text" class="form-control" id="author" required />
            </div>
            <div class="col-md-6">
              <label for="pages" class="form-label">No. of pages:</label>
              <input v-model="pages" type="number" class="form-control" id="pages" required />
            </div>
            <div class="col-md-6">
              <label for="content" class="form-label">Content:</label>
              <input v-model="content" type="text" class="form-control" id="content" required />
            </div>
            <div class="col-md-6">
                <label for="sectionList" class="form-label">Section:</label>
                <select v-model="selectedSection" class="form-select" id="sectionList" required>
                <option disabled value="">Select Section:</option>
                <option v-for="section in all_sections" :key="section.id" :value="section.id">{{ section.name }}</option>
                </select>
            </div>
            <div class="col-12 mt-3">
              <button type="submit" class="btn btn-primary">Submit</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
export default {
  data() {
    return {
      bookTitle: '',
      author: '',
      pages: null,
      content: '',
      selectedSection: null,
      all_sections: [],
    };
  },
  created() {
    this.getSections();
    const sectionId = this.$route.params.id;
    console.log(sectionId)
    if (sectionId) {
      this.selectedSection = sectionId;
      console.log(this.selectedSection);
    }
  },
  methods: {
    getSections() {
      fetch('http://127.0.0.1:5000/view_all_sections', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
      })
        .then(response => response.json())
        .then(data => {
          this.all_sections = data.all_sections;
        })
        .catch(error => {
          console.error('Error:', error);
        });
    },
    addBook() {
      fetch(`http://127.0.0.1:5000/${this.selectedSection}/add_book`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
        },
        body: JSON.stringify({
          title: this.bookTitle,
          author: this.author,
          pages: this.pages,
          content: this.content,
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