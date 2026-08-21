$ErrorActionPreference = "Stop"

if (-not (Get-Command javac -ErrorAction SilentlyContinue)) {
    throw "未找到 javac。请安装 JDK 8+，并把 JDK 的 bin 目录加入 PATH。"
}

$projectDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$outDir = Join-Path $projectDir "out"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

javac -encoding UTF-8 -d $outDir (Join-Path $projectDir "src\OrderedSyncDemo.java")
if ($LASTEXITCODE -ne 0) {
    throw "Java 编译失败"
}

java -cp $outDir OrderedSyncDemo
if ($LASTEXITCODE -ne 0) {
    throw "演示程序运行失败"
}
