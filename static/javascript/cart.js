document.addEventListener("DOMContentLoaded", () => {
  const cartItemsContainer = document.querySelector(".cart-items");
  const subtotalElement = document.querySelector(".subtotal-amount");

  // Sample items data - this could come from an API or form inputs
  const items = [
      { name: "Bamboo Plant", price: 20.00, originalPrice: 29.95, img: "/images/bamboo.jpeg" },
      { name: "Black Pepper", price: 20.00, originalPrice: 34.95, img: "/images/Black Pepper.jpeg" },
      { name: "Beetroot", price: 20.00, originalPrice: 34.95, img: "/images/beetroot.jpeg" },
      { name: "Cabbage", price: 20.00, originalPrice: 34.95, img: "/images/Cabbage.jpeg" },
      { name: "Chilli", price: 20.00, originalPrice: 34.95, img: "/images/chilli.jpeg" },
      { name: "Chilli", price: 20.00, originalPrice: 34.95, img: "/images/chilli.jpeg" }
  ];

  // Function to add an item to the cart
  function addItemToCart(item) {
      const itemCard = document.createElement("div");
      itemCard.classList.add("cart-item");
      itemCard.innerHTML = `
          
      `;

      // Event listeners for quantity controls and delete button
      const decreaseButton = itemCard.querySelector(".decrease");
      const increaseButton = itemCard.querySelector(".increase");
      const quantityInput = itemCard.querySelector('input[type="number"]');
      const deleteButton = itemCard.querySelector(".delete");

      decreaseButton.addEventListener("click", () => {
          if (quantityInput.value > 1) {
              quantityInput.value = parseInt(quantityInput.value) - 1;
              updateSubtotal();
          }
      });

      increaseButton.addEventListener("click", () => {
          quantityInput.value = parseInt(quantityInput.value) + 1;
          updateSubtotal();
      });

      quantityInput.addEventListener("input", () => {
          if (quantityInput.value < 1) quantityInput.value = 1;
          updateSubtotal();
      });

      deleteButton.addEventListener("click", () => {
          itemCard.remove();
          updateSubtotal();
      });

      cartItemsContainer.appendChild(itemCard);
      updateSubtotal();
  }

  // Function to update the subtotal
  function updateSubtotal() {
      let subtotal = 0;
      const cartItems = document.querySelectorAll(".cart-item");
      cartItems.forEach((item) => {
          const priceElement = item.querySelector(".price");
          const quantityElement = item.querySelector('input[type="number"]');
          const price = parseFloat(priceElement.textContent.match(/\$([\d.]+)/)[1]);
          const quantity = parseInt(quantityElement.value);
          subtotal += price * quantity;
      });
      subtotalElement.textContent = `$${subtotal.toFixed(2)}`;
  }

  // Adding items to the cart
  items.forEach(item => addItemToCart(item));
});
