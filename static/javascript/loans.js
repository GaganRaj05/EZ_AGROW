function showLoans(category) {
    const loanContainer = document.getElementById("loanContainer");
  
    let loansData = {
      home: [
        {
          title: "Agricultural Credit PSBS Loan",
          description: "Agricultural credit in India is a vital part of supporting the agricultural sector. Financial assistance to farmers and agricultural businesses to support various farming activities, including crop production, equipment purchase, and development.",
          link: "https://www.psbloansin59minutes.com/home",
        },
        {
          title: "KCC Kisan Credit Card Loan",
          description: "The Kisan Credit Card scheme is one of the most popular and widely used crop loan schemes in India, including Karnataka. It provides farmers with a flexible line of credit that can be used to meet their crop production needs.",
          link: "https://sbi.co.in/web/agri-rural/agriculture-banking/crop-loan/kisan-credit-card",
          image: "{{ url_for('static', filename='images/kcc.jpeg') }}", // Replace with actual image URL

        },
        {
          title: "State Bank of India",
          description: "The Kisan Credit Card scheme is one of the most popular and widely used crop loan schemes in India, including Karnataka. It provides farmers with a flexible line of credit that can be used to meet their crop production needs.",
          link: "https://sbi.co.in/web/agri-rural/agriculture-banking/crop-loan",

        },
        {
          title: "Regional Rural Banks and Cooperative Banks",
          description: "The Pradhan Mantri Fasal Bima Yojana (PMFBY) is an Indian government scheme launched in 2016 aimed at providing crop insurance to farmers. The main objective of this program is to protect farmers from financial losses due to crop failures caused by natural calamities, pests, and diseases.",
          link: "https://pmfby.gov.in",

        },
        {
          title: "National Bank for Agriculture and Rural Development (NABARD) schemes",
          description: "NABARD offers various schemes and programs designed to enhance agricultural productivity, support rural development, and improve the livelihoods of rural communities. Here are some prominent NABARD schemes:",
          link: "https://www.nabard.org/content1.aspx?id=23&catid=23&mid=530",

        },
        {
          title: "Scheme for Loan Against Sovereign Gold Bonds",
          description: "Sovereign Gold Bonds provide a way for bondholders to obtain loans by pledging their bonds as collateral. This scheme allows bondholders to leverage their gold investments without having to liquidate them.",
          link: "https://www.unionbankofindia.co.in/english/scheme-for-loan-against-sovereign-gold-bonds.aspx",

        },
      ],
  
      machinary: [
        {
          title: "Tractor Loan",
          description: "This loan helps farmers purchase a new or used tractor. Tractors are essential for various farming activities like plowing, tilling, and planting. The loan usually covers up to 80-90% of the tractor's cost, with flexible repayment options.",
          link: "https://www.hdfcbank.com/personal/borrow/popular-loans/ruralloans/tractor-loan",

        },
        {
            title: "Combined Harvest Loan",
            description: "Combine harvesters are machines used to harvest crops efficiently. This loan enables farmers to buy a combine harvester, which combines reaping, threshing, and winnowing into a single process. The loan often covers a significant portion of the machine's cost.",
            link: "https://www.google.co.in/aclk?sa=L&ai=DChcSEwiW9pfFmaaIAxXSq2YCHZhmAf0YABACGgJzbQ&ae=2&co=1&gclid=CjwKCAjwxNW2BhAkEiwA24Cm9DfE-rVcyVjKcz_7UvVdHmfTizidLgWSojYGwemQUk2hc-uqA3lr4hoCVc8QAvD_BwE&sig=AOD64_3cHK-J1TD1TBsdhXe_P2xVMKOAiA&q&adurl&ved=2ahUKEwjA4ZDFmaaIAxWY1jgGHfIGIi4Q0Qx6BAgLEAE",

          },
          {
            title: " Power Tiller Loan",
            description: "Power tillers are smaller machines used for soil preparation, especially in smaller fields. This loan helps farmers purchase a power tiller, making soil preparation easier and faster. The loan can be used to buy new or used power tillers.",
            link: "https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://sbi.co.in/web/agri-rural/financing-power-tiller&ved=2ahUKEwirmvWXm6aIAxVGyqACHQR8OYkQFnoECA4QAQ&usg=AOvVaw0EIGjAz8Bne5LGYd4Q8ONR",
          },
          {
            title: "TDairy and Livestock Equipment Loan",
            description: "This loan helps farmers engaged in dairy farming or livestock rearing to buy machinery like milking machines, feed grinders, and cooling units. The loan aims to increase ",
            link: "hhttps://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.bajajfinserv.in/dairy-farm-loan%23:~:text%3DBajaj%2520Finance%2520offers%2520dairy%2520farm,%252C%2520livestock%252C%2520feed%252C%2520etc.&ved=2ahUKEwimsIKPnKaIAxVL1zgGHdogDBYQFnoECA0QAw&usg=AOvVaw09MhDyYV0ABOw1l3qzqGjk",
          },
      ],
    };
  
    loanContainer.innerHTML = ""; // Clear previous content
  
    loansData[category].forEach((loan) => {
      let loanBox = document.createElement("div");
      loanBox.className = "loan-box";
      loanBox.innerHTML = `
        <h3>${loan.title}</h3>
        <p>${loan.description}</p>
        <div class="loan-actions">
          <a href="${loan.link}" class="apply-link" target="_blank">Apply Now</a>
        </div>
      `;
  
      loanContainer.appendChild(loanBox);
    });
  }
  
  // Trigger the "home" category as the default active category on page load
  window.onload = function () {
    showLoans("home");
  };
  