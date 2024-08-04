<template>
  <div>
    <NavComp/>
  <div>
    <h1>Library App</h1>
    <div>
    <table class="tablestyle">
      <tr>
        <td style="padding: 100px;"><a href="/#/register">Register</a></td>
        <td style="padding: 100px;"><a href="/#/login">Login</a></td>
      </tr>
    </table>
  </div>
  </div>
</div>
</template>

<script>
import NavComp from '@/components/NavComp.vue'

export default {
  name: 'HomeView',
  components: {
    NavComp
  }
}
</script>

<style>
.tablestyle{
  margin-left: auto; 
  margin-right: auto; 
  width: 90%;
  font-size: 50px;
  margin-top: 50px;
  padding: 100px;
  background-color: rgb(230, 237, 240);
}
</style>
