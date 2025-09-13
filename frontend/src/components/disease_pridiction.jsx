import React, { useState } from "react";
import { Leaf, UploadCloud, X, LoaderCircle } from "lucide-react";

export function Prediction() {
    const [selectedFile, setSelectedFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [isDragging, setIsDragging] = useState(false);
    const [isLoading, setIsLoading] = useState(false);
    const [result, setResult] = useState(null);

    // Handles file selection from the file input dialog
    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (file && file.type.startsWith("image/")) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setResult(null); // Clear previous results
        } else {
            // Optional: handle non-image file selection
            alert("Please select an image file (PNG, JPG, JPEG).");
        }
    };

    // Clears the selected file and its preview
    const clearSelection = () => {
        setSelectedFile(null);
        setPreview(null);
        setResult(null);
    };

    // --- Drag and Drop Handlers ---
    const handleDragOver = (e) => {
        e.preventDefault(); // Necessary to allow dropping
        setIsDragging(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        setIsDragging(false);
    };

    const handleDrop = (e) => {
        e.preventDefault();
        setIsDragging(false);
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith("image/")) {
            setSelectedFile(file);
            setPreview(URL.createObjectURL(file));
            setResult(null);
        }
    };
    
    // --- Form Submission Handler ---
    const handleSubmit = (e) => {
        e.preventDefault();
        if (!selectedFile) {
            alert("Please select a file to predict.");
            return;
        }
        setIsLoading(true);
        setResult(null);

        // Simulate a network request to the backend model
        setTimeout(() => {
            // In a real application, you would make an API call here
            // with the `selectedFile` and get a real result.
            setResult({
                disease: "Tomato Late Blight",
                confidence: "95.8%",
                recommendation: "Apply a fungicide containing mancozeb or chlorothalonil. Ensure proper plant spacing for better air circulation to reduce humidity."
            });
            setIsLoading(false);
        }, 2000); // 2-second delay for simulation
    };


    return (
        <form onSubmit={handleSubmit} className="text-center">
            <h3 className="text-2xl font-bold text-gray-800 mb-4">Instantly Identify Plant Diseases</h3>
            <p className="text-gray-600 mb-6 max-w-xl mx-auto">
                Upload a clear photo of a plant's leaf, and our advanced image recognition model will detect potential diseases, providing you with early warnings and treatment advice.
            </p>

            {/* --- File Input & Dropzone --- */}
            <div
                onDragOver={handleDragOver}
                onDragLeave={handleDragLeave}
                onDrop={handleDrop}
                className={`relative border-4 border-dashed rounded-2xl p-8 transition-colors ${
                    isDragging ? 'border-green-600 bg-green-50' : 'border-gray-300 hover:border-green-500'
                }`}
            >
                {/* --- Image Preview --- */}
                {preview ? (
                    <>
                        <img src={preview} alt="Selected leaf" className="w-full h-48 object-contain mx-auto rounded-md" />
                        <button
                            type="button"
                            onClick={clearSelection}
                            className="absolute top-2 right-2 bg-white rounded-full p-1.5 shadow-md hover:bg-red-100 text-gray-600 hover:text-red-600 transition-colors"
                            aria-label="Clear selection"
                        >
                            <X size={20} />
                        </button>
                    </>
                ) : (
                    <>
                        <UploadCloud className="h-16 w-16 text-gray-400 mx-auto mb-4" />
                        <p className="text-gray-700 font-semibold mb-2">Drag & drop a file here or</p>
                        <label htmlFor="file-upload" className="text-green-600 font-bold cursor-pointer hover:underline">
                            Choose a file
                        </label>
                    </>
                )}
                <input id="file-upload" type="file" className="hidden" onChange={handleFileChange} accept="image/png, image/jpeg, image/jpg" />
            </div>
            {selectedFile && !result && (
                <p className="text-sm text-gray-500 mt-3">
                    File selected: <strong>{selectedFile.name}</strong>
                </p>
            )}

            {/* --- Submit Button --- */}
            <button
                type="submit"
                disabled={!selectedFile || isLoading}
                className="w-full mt-6 bg-green-600 text-white font-bold py-3 px-6 rounded-lg hover:bg-green-700 transition-colors disabled:bg-gray-400 disabled:cursor-not-allowed flex items-center justify-center"
            >
                {isLoading ? (
                    <>
                        <LoaderCircle className="animate-spin mr-2" />
                        Analyzing...
                    </>
                ) : (
                    'Get Prediction'
                )}
            </button>
            
            {/* --- Result Display --- */}
            {result && (
                <div className="mt-8 text-left p-6 bg-green-50 border border-green-200 rounded-lg">
                    <h4 className="text-xl font-bold text-gray-800">Prediction Result</h4>
                    <p className="mt-2"><strong>Disease:</strong> <span className="text-red-600 font-semibold">{result.disease}</span></p>
                    <p className="mt-1"><strong>Confidence:</strong> {result.confidence}</p>
                    <p className="mt-4 font-semibold text-gray-700">Recommendation:</p>
                    <p className="text-gray-600">{result.recommendation}</p>
                </div>
            )}
        </form>
    );
}