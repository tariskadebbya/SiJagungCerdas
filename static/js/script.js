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

    if (!file.type.startsWith("image/")) {
      alert("File harus berupa gambar!");
      input.value = "";
      return;
    }

    selectedFile = file;

    if (previewImage) {
      previewImage.src = URL.createObjectURL(file);
      previewImage.style.display = "block";
    }

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

      console.log("Hasil Prediksi:", data);

      /**
       * ==========================================
       * ERROR BACKEND
       * ==========================================
       */
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
       * HASIL PREDIKSI
       * ==========================================
       */
      let kelas = data.kelas;

      if (kelas === "Bukan Jagung") {

        diseaseName.textContent =
          "❌ Gambar Bukan Daun Jagung";

      } else if (kelas === "Hawar") {

        diseaseName.textContent =
          "🌽 Penyakit: Hawar Daun";

      } else if (kelas === "Karat") {

        diseaseName.textContent =
          "🌽 Penyakit: Karat Daun";

      } else if (kelas === "Sehat") {

        diseaseName.textContent =
          "🌿 Daun Jagung Sehat";

      } else {

        diseaseName.textContent =
          `🌽 Hasil Deteksi: ${kelas}`;
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