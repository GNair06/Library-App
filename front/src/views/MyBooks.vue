<template>
  <div>
  <NavComp/>
  <div style="padding: 10px;">
      <h2>My Books</h2><br>
      <table style="margin: auto;">

          <tr v-for="item in lst" :key="item.id">
            <div v-if="(this.id == item.user_id)">
              <td style="padding: 10px;"><b>Title:</b> {{ item.title }}</td>
              <td style="padding: 10px;"><b>Author:</b> {{ item.author }}</td>
              <td style="padding: 10px;"><b>No. of pages:</b> {{ item.pages }}</td>
              <td style="padding: 10px;"><b>Date:</b> {{ item.date }}</td>
              <td>
                <router-link :to="`/view_book_content/${ item.book_id }`"><b>View Content</b></router-link>
              </td>
            </div>
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
      this.getLst();
  },
  components: {
      NavComp
  },
  methods: {
      getLst(){
          const token = localStorage.getItem("access_token");
          console.log(token);
          fetch("http://127.0.0.1:5000/view_my_issues",{
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
  }
  
}
</script>