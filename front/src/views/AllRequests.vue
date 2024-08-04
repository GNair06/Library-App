<template>
    <div>
    <NavComp/>
    <div style="padding: 10px;">
        <h2>All Requests</h2><br>
        <table style="margin: auto;">
            <tr v-for="item in lst" :key="item.id">
                <td style="padding: 10px;"><b>Title:</b> {{ item.title }}</td>
                <td style="padding: 10px;"><b>Author:</b> {{ item.author }}</td>
                <td style="padding: 10px;"><b>No. of pages:</b> {{ item.pages }}</td>
                <td style="padding: 10px;"><b>Requested by:</b> {{ item.user_name }}</td>
                <td v-if="(this.role=='librarian')">
                    <button class="btn" @click="IssueBook(item.id)">Issue</button>
                </td>
                <td v-if="(this.role=='librarian')">
                    <button class="btn" @click="Reject(item.id)">Reject</button>
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
        lst: []
    };
    },
    mounted(){
        this.getAllRequests();
    },
    components: {
        NavComp
    },
    methods: {
        getAllRequests(){
            const token = localStorage.getItem("access_token");
            console.log(token);
            fetch("http://127.0.0.1:5000/view_all_requests",{
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
                this.lst = data.lst;
                console.log(this.all_lst)
            })
            .catch(error => {
                console.log(error);
            })
        },
        IssueBook(ReqId) {
            fetch(`http://127.0.0.1:5000/issue_book/` + ReqId, {
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
            console.log(`issued successfully`);
            this.getAllRequests();
            })
            .catch(error => {
            console.error(`Error:`, error);
            });
        },
        Reject(ReqId) {
            fetch(`http://127.0.0.1:5000/reject_request/` + ReqId, {
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
            console.log(`request rejected`);
            this.getAllRequests();
            })
            .catch(error => {
            console.error(`Error:`, error);
            });
        },
    }
    
}
</script>