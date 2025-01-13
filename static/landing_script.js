jQuery(".property-slide").slick({
    dots: false,
    infinite: true,
    speed: 300,
    slidesToShow: 3,
    slidesToScroll: 2,
    arrows: true,
    autoplay: true,
    autoplaySpeed: 6000,
    prevArrow:
    '<button class="slick-prev fa-solid fa-arrow-left" aria-label="Prev" style="color: white;"></button>',
    nextArrow:
      '<button class="slick-next fa-solid fa-arrow-right" aria-label="Next"></button>',
    responsive: [
      {
        breakpoint: 992,
        settings: {
          slidesToShow: 2,
          slidesToScroll: 2
        }
      },
      {
        breakpoint: 600,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      },
      {
        breakpoint: 480,
        settings: {
          slidesToShow: 1,
          slidesToScroll: 1
        }
      }
      // You can unslick at a given breakpoint now by adding:
      // settings: "unslick"
      // instead of a settings object
    ]
  });
  const urlParams = new URLSearchParams(window.location.search);
  if (urlParams.get('show_modal') === 'true') {
    console.log("logreg modall called from landing script")
    openLogRegModal(); // Call the function to open the modal
  }