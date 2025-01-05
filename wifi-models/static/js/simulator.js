document.getElementById('simForm').onsubmit = async (e) => {
    e.preventDefault();
    const form = new FormData(e.target);
    const img = document.getElementById('resultImage');
    const loading = document.getElementById('loading');
    const submitBtn = document.getElementById('submitBtn');
    
    try {
        loading.style.display = 'block';
        img.style.display = 'none';
        submitBtn.disabled = true;
        
        const response = await fetch('/simulate', {
            method: 'POST',
            body: form
        });
        
        if (!response.ok) {
            throw await response.text();
        }
        
        const blob = await response.blob();
        img.src = URL.createObjectURL(blob);
        img.style.display = 'block';
    } catch (error) {
        alert(error);
    } finally {
        loading.style.display = 'none';
        submitBtn.disabled = false;
    }
};
