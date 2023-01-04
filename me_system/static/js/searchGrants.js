const searchField = document.querySelector("#searchField");

const tableOutput=document.querySelector(".table-output");
const appTable=document.querySelector(".app-table");
const tbody=document.querySelector(".table-body");
const paginationContainer=document.querySelector('.pagination-container');

tableOutput.style.display="none";

searchField.addEventListener("keyup", (e) => {
  const searchValue = e.target.value;

  if (searchValue.trim().length > 0) {
    paginationContainer.style.display='none';
    tbody.innerHTML="";
  
    fetch("search-grants", {
      body: JSON.stringify({ searchText: searchValue }),
      method: "POST",
    })
      .then((res) => res.json())
      .then((data) => {
        console.log('data',data);
        appTable.style.display='none';
        tableOutput.style.display="block";
        if (data.length==0){
            tableOutput.innerHTML='No result found';
        }
        else{
            data.forEach(item => {
                tbody.innerHTML +=`
                <tr>
                    <td>${item.project_name}</td>
                    <td>${item.thematic}</td>
                    <td>${item.donor}</td>
                    <td>${item.project_start}</td>
                    <td>${item.project_end}</td>
                    <td>${item.person_responsible}</td>
                    <td>${item.info}</td>
                    <td>${item.name}</td>

                </tr>`
            });
        }
        });
      }

  else{
    tableOutput.style.display='none';
    paginationContainer.style.display="block";
    appTable.style.display="block";
  }
});