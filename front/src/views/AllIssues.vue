<template>
    <div>
    <NavComp/>
    <div style="padding: 10px;">
        <h2>All Issues</h2><br>
        <table style="margin: auto;">
            <tr v-for="item in lst" :key="item.id">
                <td style="padding: 10px;"><b>Title:</b> {{ item.title }}</td>
                <td style="padding: 10px;"><b>Author:</b> {{ item.author }}</td>
                <td style="padding: 10px;"><b>No. of pages:</b> {{ item.pages }}</td>
                <td style="padding: 10px;"><b>Date:</b> {{ item.date }}</td>
                <td style="padding: 10px;"><b>Issued by:</b> {{ item.user_name }}</td>
                <td v-if="(this.role=='librarian')">
                    <button class="btn" @click="Revoke(item.id)"><b>Revoke</b></button>
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
        this.getAllIssues();
    },
    components: {
        NavComp
    },
    methods: {
        getAllIssues(){
            const token = localStorage.getItem("access_token");
            console.log(token);
            fetch("http://127.0.0.1:5000/view_all_issues",{
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
                console.log(this.lst)
            })
            .catch(error => {
                console.log(error);
            })
        },
        Revoke(IssueId) {
            fetch(`http://127.0.0.1:5000/revoke_access/` + IssueId, {
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
            console.log(`access revoked`);
            this.getAllIssues();
            })
            .catch(error => {
            console.error(`Error:`, error);
            });
        },
    }
    
}
</script>