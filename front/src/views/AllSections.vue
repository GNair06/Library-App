<template>
    <div>
    <NavComp/>
    <div style="padding: 10px;">
        <h2>All Sections</h2><br>
        <div v-if="(this.role=='librarian')">
                    <router-link :to="`/create_section`"><b>Create Section</b></router-link><br>
        </div>
        <table class="table">
            <tr v-for="section in all_sections" :key="section.id">
                <td style="padding: 10px;"><b>Section Name: </b>{{ section.name }}</td>
                <td style="padding: 10px;">
                    <router-link :to="`/books_of_section/${section.id}`"><b>View Books</b></router-link>
                </td>
                <td v-if="(this.role=='librarian')" style="padding: 10px;">
                    <router-link :to="`/${section.id}/add_book`"><b>Add Book</b></router-link>
                </td>
                <td v-if="(this.role=='librarian')" style="padding: 10px;">
                    <router-link :to="`/edit_section/${section.id}`"><b>Edit</b></router-link>
                </td>
                <td v-if="(this.role!='user')" style="padding: 10px;">
                    <button class="btn" @click="DeleteSection(section.id)"><b>Delete</b></button>
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
        all_sections: []
    };
    },
    mounted(){
        this.getAllSections();
    },
    components: {
        NavComp
    },
    methods: {
        getAllSections(){
            const token = localStorage.getItem("access_token");
            console.log(token);
            fetch("http://127.0.0.1:5000/view_all_sections",{
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
                this.all_sections = data.all_sections;
                console.log(this.all_sections)
            })
            .catch(error => {
                console.log(error);
            })
        },

        DeleteSection(SecId) {
            fetch(`http://127.0.0.1:5000/delete_section/` + SecId, {
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
            this.getAllSections();
            })
            .catch(error => {
            console.error(`Error:`, error);
            });
    },
    }
    
}
</script>