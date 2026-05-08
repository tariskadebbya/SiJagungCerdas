/**
 * ==========================================
 * INIT
 * ==========================================
 */
document.addEventListener("DOMContentLoaded", function () {

  /**
   * ==========================================
   * HAMBURGER MENU
   * ==========================================
   */
  const menuToggle = document.getElementById("mobile-menu");
  const navMenu = document.querySelector(".nav-menu");

  if (menuToggle && navMenu) {
    menuToggle.addEventListener("click", () => {
      navMenu.classList.toggle("active");
    });
  }

  /**
   * ==========================================
   * DOM ELEMENT
   * ==========================================
   */
  const uploadGallery = document.getElementById("uploadGallery");
  const openCamera = document.getElementById("openCamera");

  const previewImage = document.getElementById("previewImage");

  const resultBox = document.getElementById("resultBox");
  const diseaseName = document.getElementById("diseaseName");
  const confidenceText = document.getElementById("confidence");

  let selectedFile = null;

  /**
   * ==========================================
   * HANDLE FILE
   * ==========================================
   */
  function handleFile(input) {

    const file = input.files[0];

    if (!file) return;

    // Validasi gambar
    if (!file.type.startsWith("image/")) {
      alert("File harus berupa gambar!");
      input.value = "";
      return;
    }

    selectedFile = file;

    // Preview gambar
    if (previewImage) {
      previewImage.src = URL.createObjectURL(file);
      previewImage.style.display = "block";
    }

    // Reset hasil lama
    if (resultBox) {
      resultBox.style.display = "none";
    }
  }

  /**
   * ==========================================
   * EVENT INPUT
   * ==========================================
   */
  if (uploadGallery) {
    uploadGallery.addEventListener("change", function () {
      handleFile(this);
    });
  }

  if (openCamera) {
    openCamera.addEventListener("change", function () {
      handleFile(this);
    });
  }

  /**
   * ==========================================
   * PREDICT FUNCTION
   * ==========================================
   */
  window.predict = async function () {

    if (!selectedFile) {
      alert("Silakan pilih gambar terlebih dahulu!");
      return;
    }

    const formData = new FormData();
    formData.append("image", selectedFile);

    // Tampilkan loading
    if (resultBox) {
      resultBox.style.display = "block";
    }

    if (diseaseName) {
      diseaseName.textContent = "⏳ Sedang menganalisis gambar...";
    }

    if (confidenceText) {
      confidenceText.textContent = "";
    }

    try {

      const response = await fetch("/predict", {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      console.log(data);

      // Error backend
      if (!response.ok) {

        if (diseaseName) {
          diseaseName.textContent = "❌ Terjadi kesalahan";
        }

        if (confidenceText) {
          confidenceText.textContent =
            data.error || "Server gagal memproses";
        }

        return;
      }

      /**
       * ==========================================
       * HASIL NON JAGUNG
       * ==========================================
       */
      if (data.status === "non_jagung") {

        if (diseaseName) {
          diseaseName.textContent =
            "❌ Gambar bukan daun jagung";
        }

        if (confidenceText) {
          confidenceText.textContent =
            `Tingkat Kepercayaan: ${data.confidence}%`;
        }

        return;
      }

      /**
       * ==========================================
       * HASIL JAGUNG
       * ==========================================
       */
      if (diseaseName) {

        let penyakit = data.penyakit;

        // Format nama penyakit
        if (penyakit === "hawar_daun") {
          penyakit = "Hawar Daun";
        }
        else if (penyakit === "karat_daun") {
          penyakit = "Karat Daun";
        }
        else if (penyakit === "sehat") {
          penyakit = "Daun Sehat";
        }

        diseaseName.textContent =
          `🌽 Penyakit: ${penyakit}`;
      }

      if (confidenceText) {
        confidenceText.textContent =
          `Tingkat Kepercayaan: ${data.confidence}%`;
      }

    }
    catch (error) {

      console.error(error);

      if (diseaseName) {
        diseaseName.textContent =
          "❌ Server tidak merespon";
      }

      if (confidenceText) {
        confidenceText.textContent =
          "Periksa koneksi atau backend Flask";
      }
    }
  };

});