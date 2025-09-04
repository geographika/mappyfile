# ./validate_schemas.ps1

function Validate-SchemaFolder {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Folders
    )

    foreach ($SchemaFolder in $Folders) {
        Write-Host "Validating schemas in folder: $SchemaFolder" -ForegroundColor Cyan

        # Loop through all JSON files
        Get-ChildItem -Path $SchemaFolder -Filter *.json | ForEach-Object {
            $file = $_.FullName

            try {
                python -c "import json, sys; from jsonschema import Draft202012Validator; Draft202012Validator.check_schema(json.load(open(r'$file')))" 
                Write-Host "$file is valid" -ForegroundColor Green
            } catch {
                Write-Host "$file is INVALID" -ForegroundColor Red
            }
        }
    }
}

mappyfile schema docs/schemas/mapfile-latest.json
mappyfile schema docs/schemas/mapfile-schema-7-6.json --version=7.6
mappyfile schema docs/schemas/mapfile-schema-8-0.json --version=8.0
mappyfile schema docs/schemas/mapfile-schema-8-2.json --version=8.2
mappyfile schema docs/schemas/mapfile-schema-8-4.json --version=8.4

Validate-SchemaFolder -Folders "mappyfile/schemas","docs/schemas"