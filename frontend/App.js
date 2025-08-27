import React from 'react';
import './App.css';

function App() {
  return (
    <div className="container">
      {/* Header */}
      <div style={{display:'flex',alignItems:'center',justifyContent:'center',gap:'1em',marginBottom:'1em'}}>
        <span style={{fontFamily:'Poppins,Arial,sans-serif',fontSize:'2em',fontWeight:700,letterSpacing:'1px'}}>
          <span style={{color:'#3d3dd7'}}>Sab</span><span style={{color:'#ff9800'}}>Paisa</span>
          <span style={{color:'#0a3c7d'}}> DJB Refund Dashboard</span>
        </span>
      </div>
      {/* Upload Section */}
      <h2>1. Upload Excel</h2>
      <label htmlFor="excelFile" style={{fontWeight:600,color:'#0a3c7d'}}>Select Excel File:</label>
      <input type="file" id="excelFile" accept=".xlsx,.xls" aria-label="Upload Excel File" />
      <button type="button">Upload</button>
      <div id="uploadStatus"></div>
      <div className="spinner" id="spinner"></div>
      {/* Search Section */}
      <h2>2. Search Transactions</h2>
      <div style={{marginBottom:'0.5em',color:'#0a3c7d',fontSize:'1.08em',fontWeight:600}}>
        <span>Tip: You can search by <b>Transaction ID</b>, <b>clienttransId</b>, or <b>Bidding Firm Name</b>. Leave any field blank if not needed.</span>
      </div>
      <hr style={{border:'none',borderTop:'2px solid #eaf6fb',margin:'1em 0 2em 0'}} />
      <div style={{display:'flex',alignItems:'center',gap:'1em',marginBottom:'2em',flexWrap:'wrap'}}>
        <input type="text" id="searchId" placeholder="Transaction ID" style={{flex:1,minWidth:'180px'}} aria-label="Transaction ID" />
        <input type="text" id="searchClientTransId" placeholder="clienttransId" style={{flex:1,minWidth:'180px'}} aria-label="clienttransId" />
        <input type="text" id="searchFirm" placeholder="Bidding Firm Name" style={{flex:1,minWidth:'180px'}} aria-label="Bidding Firm Name" />
        <button type="button">Search</button>
        <button type="button">Clear</button>
      </div>
      <div style={{marginBottom:'0.5em'}}>
        <button id="downloadBtn" style={{display:'none'}}>Download Results (CSV)</button>
        <button id="downloadExcelBtn" style={{display:'none',marginLeft:'0.5em'}}>Download Results (Excel)</button>
        <button id="downloadPDFBtn" style={{display:'none',marginLeft:'0.5em'}}>Download Results (PDF)</button>
        <span id="resultsCount" style={{marginLeft:'1em',fontWeight:600,color:'#0a3c7d'}}></span>
      </div>
      <div className="table-container">
        <div id="searchResults" style={{minHeight:'60px'}}></div>
      </div>
      {/* Receipt Section */}
      <h2>3. Generate Receipt</h2>
      <div style={{display:'flex',alignItems:'center',gap:'1em',marginBottom:'1.5em',flexWrap:'wrap'}}>
        <input type="text" id="receiptTransId" placeholder="Enter Transaction ID" style={{flex:1,minWidth:'180px'}} aria-label="Receipt Transaction ID" />
        <button type="button">Generate Receipt</button>
      </div>
      <div id="receiptSection" style={{display:'none',marginBottom:'2em'}}></div>
      <div id="toast" className="toast"></div>
      <div id="detailsModal" className="modal">
        <div className="modal-content">
          <span className="modal-close">&times;</span>
          <h2>Transaction Details</h2>
          <div id="modalBody"></div>
        </div>
      </div>
      <footer style={{textAlign:'center',padding:'1.2em 0 0.5em 0',color:'#0a3c7d',fontSize:'1em',fontWeight:600,letterSpacing:'0.5px'}}>
        &copy; 2025 SabPaisa. All Rights Reserved.
      </footer>
    </div>
  );
}

export default App;
