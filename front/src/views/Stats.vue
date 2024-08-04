<template>
    <div>
        <div v-html="sectionGraph"></div>
        <div v-html="requestedBooksGraph"></div>
        <div v-html="issuedBooksGraph"></div>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        sectionGraph: '',
        requestedBooksGraph: '',
        issuedBooksGraph: ''
      };
    },
    mounted() {
        this.ready();
        this.fetchGraphs();
    },
    methods: {
        ready(){
            const token = localStorage.getItem("access_token");
            console.log(token);
            fetch("http://127.0.0.1:5000/statistics",{
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
            .catch(error => {
                console.log(error);
            })
        },
      async fetchGraphs() {
        try {
          // Fetch requested books graph
          const requestedResponse = await fetch('http://localhost:5000/request_graph');
          const requestedData = await requestedResponse.text();
          this.requestedBooksGraph = requestedData;

          // Fetch requested books graph
          const sectionResponse = await fetch('http://localhost:5000/section_graph');
          const sectionData = await sectionResponse.text();
          this.sectionGraph = sectionData;
  
          // Fetch issued books graph
          const issuedResponse = await fetch('http://localhost:5000/issue_graph');
          const issuedData = await issuedResponse.text();
          this.issuedBooksGraph = issuedData;
        } catch (error) {
          console.error('Error fetching graphs:', error);
        }
      }
    }
  };
  </script>
  