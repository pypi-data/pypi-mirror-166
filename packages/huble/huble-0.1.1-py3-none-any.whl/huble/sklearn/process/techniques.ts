export const preprocessingTechniques = [
    {
        name: "Remove NAN values",
        value: "Remove NAN values",
        parameters: [
            {
              name: "axis",
              type: "select",
              options: [0, 1],
              default: 0,
              render: true,
            },
          ],
    },
    {
        name: "Replace NAN values",
        value: "Replace NAN values",
        parameters: [
          {
            name: "value",
            type: "any",
            render: true,
          },
          {
            name: "axis",
            type: "select",
            options: [0, 1],
            render: true,
          },
        ],
    },
    {
        name: "Dropping rows or columns",
        value: "Dropping rows or columns",
        parameters: [
          {
            name: "Labels",
            type: "any",
            render: true,
          },
          {
            name: "axis",
            type: "select",
            options: [0, 1],
            defaultValue: 0,
            render: true,
          },
        ],
    },
    {
        name: "Remove Outliers",
        value: "Remove Outliers",
        parameters: [
          {
            name: "Column Name",
            type: "string",
            render: true,
          },
        ],
    },
    {
        name: "Drop Duplicates",
        value: "Drop Duplicates",
        parameters: [
          {
            name: "subset",
            type: "columnList",
            render: true,
          },
          {
            name: "keep",
            type: "select",
            options: ['first','last', 'False'],
            default: 'first',
            render: true,
          },
        ],
    },
    {
        name: "Change Data Type",
        value: "Change Data Type",
        parameters: [
          {
            name: "Column name",
            type: "string",
            render: true,
          },
          {
            name: "data type",
            type: "string",
            render: true,
          },
        ],
    },
    {
        name: "Transform Data",
        value: "Transform Data",
        parameters: [
          {
            name: "function",
            type: "any",
            render: true,
          },
          {
            name: "axis",
            type: "select",
            options: [0,1],
            default: 0,
            render: true,
          },
        ],
    },
    {
        name: "Round a DataFrame",
        value: "Round a DataFrame",
        parameters: [
          {
            name: "decimals",
            type: "number",
            render: true,
          },
        ],
    },
    {
        name: "Filter DataFrame",
        value: "Filter DataFrame",
        parameters: [
          {
            name: "items",
            type: "list",
            render: true,
          },
          {
            name: "like",
            type: "string",
            render: true,
          },
          {
            name: "axis",
            type: "select",
            options: [0, 1, 'None'],
            default: 'None',
            render: true,
          },
        ],
    },
    {
        name: "Truncate DataFrame",
        value: "Truncate DataFrame",
        parameters: [
          {
            name: "before",
            type: "any",  //date | str | int
            render: true,
          },
          {
            name: "after",
            type: "any",  //date | str | int
            render: true,
          },
          {
            name: "axis",
            type: "select",
            options: [0, 1, 'None'],
            default: 'None',
            render: true,
          },
        ],
    },
    {
        name: "Sort Values",
        value: "Sort Values",
        parameters: [
          {
            name: "by",
            type: "string",  //str | list of str
            render: true,
          },
          {
            name: "ascending",
            type: "select", 
            options: [true, false],
            default: true,
            render: true,
          },
          {
            name: "axis",
            type: "select",
            options: [0, 1],
            default: 0,
            render: true,
          },
        ],
    },
    {
        name: "Transpose DataFrame",
        value: "Transpose DataFrame",
    },
    {
        name: "Normalization",
        value: "Normalization",
        parameters: [
          {
            name: "column name",
            type: "string", 
            render: true,
          },
          {
            name: "method",
            type: "select", 
            options: ['Maximum Absolute Scaling', 'Min-Max Feature Scaling','Z-score'],
            render: true,
          },
        ],
    },
    {
        name: "Binning",
        value: "Binning",
        parameters: [
          {
            name: "column name",
            type: "string", 
            render: true,
          },
          {
            name: "bins",
            type: "any",  //int, sequence of scalars 
            render: true,
          },
          {
            name: "labels",
            type: "array",   
            render: true,
          },
        ],
    },
    {
        name: "One Hot Encoding",
        value: "One Hot Encoding",
        parameters: [
          {
            name: "column name",
            type: "string", 
            render: true,
          },
        ],
    },
    {
        name: "Feature Hashing",
        value: "Feature Hashing",
        parameters: [
          {
            name: "n_features",
            type: "number", 
            default: 2**20,
            render: true,
          },
          {
            name: "input_type",
            type: "string", //default: dict 
            render: true,
          },
        ],
    },
]
