$lessonsDir = "c:\Users\avery\Desktop\Free CS Math\CSMathClass\lessons"

# Find all Day*.html files
$files = Get-ChildItem -Path $lessonsDir -Recurse -Filter "Day*.html"

Write-Host "File,Lines,HasHeroMeta,HasTOC,InfoBlocks,CodeBlocks,VideoCount,HasQuiz"

foreach ($file in $files) {
    $content = Get-Content -Path $file.FullName -Raw
    $lines = (Get-Content -Path $file.FullName).Count
    
    # Check for hero-meta
    $hasHeroMeta = $content -match "hero-meta|meta-item"
    
    # Check for TOC
    $hasTOC = $content -match "toc-list|toc-link"
    
    # Count info blocks
    $infoBlocks = ([regex]::Matches($content, '<div class="info">').Count)
    
    # Count code blocks
    $codeBlocks = ([regex]::Matches($content, '<pre class="code-block">').Count) + 
    ([regex]::Matches($content, '<code class').Count)
    
    # Count video references
    $videoCount = ([regex]::Matches($content, 'vid:\s*[''"][^''"]+[''"]').Count) +
    ([regex]::Matches($content, 'youtube\.com').Count)
    
    # Has quiz section
    $hasQuiz = $content -match "quizContainer|initQuiz"
    
    Write-Host "$($file.Name),$lines,$hasHeroMeta,$hasTOC,$infoBlocks,$codeBlocks,$videoCount,$hasQuiz"
}
