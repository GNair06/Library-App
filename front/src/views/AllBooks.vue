<template>
    <div>
    <NavComp/>
    <div style="padding: 10px;">
        <h2>All Books</h2><br>
        <table class="table">
            <tr v-for="book in all_books" :key="book.id">
                <td><b>Title:</b> {{ book.title }}</td>
                <td><b>Author:</b> {{ book.author }}</td>
                <td><b>No. of pages:</b> {{ book.pages }}</td>
                <td v-if="(this.role!='user')">
                    <router-link :to="`/view_book_content/${ book.id }`"><b>View Content</b></router-link>
                </td>
                <td v-if="(this.role=='librarian')">
                    <router-link :to="`/edit_book/${book.id}`"><b>Edit</b></router-link>
                </td>
                <td v-if="(this.role!='user')">
                    <button class="btn" @click="DeleteBook(book.id)"><b>Delete</b></button>
                </td>
                <td v-if="(this.role=='user')">
                    <button class="btn" @click="ReqBook(book.id)"><b>Request</b></button>
                </td>
            </tr>
        </table>
    </div>
</div>
</template>

<script>
import NavComp from '@/components/NavComp.vue'
import UserMixin from '../mixins_folder/UserMixin'
export default{
    mixins: [UserMixin],
    data(){
        return {
        all_books: []
    };
    },
    mounted(){
        this.getAllBooks();
    },
    components: {
        NavComp
    },
    methods: {
        getAllBooks(){
            const token = localStorage.getItem("access_token");
            console.log(token);
            fetch("http://127.0.0.1:5000/view_all_books",{
                method: "GET",
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': 'Bearer ' + localStorage.getItem("access_token"),
                },
            })
            .then(resp => {
                console.log(resp);
                return resp.json();
            })
            .then(data => {
                console.log(data);
                this.all_books = data.all_books;
                console.log(this.all_books)
            })
            .catch(error => {
                console.log(error);
            })
        },

        DeleteBook(BookId) {
            fetch(`http://127.0.0.1:5000/delete_book/` + BookId, {
            method: 'DELETE',
            headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json',
            },
        })
            .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            console.log(`deleted successfully`);
            this.getAllBooks();
            })
            .catch(error => {
            console.error(`Error:`, error);
            });
    },

    ReqBook(BookId) {
            fetch(`http://127.0.0.1:5000/request_book/` + BookId, {
            method: 'POST',
            headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json',
            },
        })
            .then(response => {
            if (!response.ok) {
                throw new Error(`Error: ${response.status}`);
            }
            console.log(`request made successfully`);
            this.getAllBooks();
            })
            .catch(error => {
            console.error(`Error:`, error);
            });
    },

    }
    
}
</script>